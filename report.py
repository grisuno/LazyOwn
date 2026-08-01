#!/usr/bin/env python3
"""
LazyOwn Security Intelligence Report
Executive metrics generator for Cybersecurity Management
KPIs, OKRs, threat detection and forensic analysis
"""

import csv
import io
import json
import os
import re
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402

# --- HARDWARE OPTIMIZATION (Tiger Lake i3) ---
torch.set_num_threads(4)
os.environ["KMP_BLOCKTIME"] = "1"

# =============================================================================
# 1. RESMA GEOMETRIC ENGINE (THE BRAIN)
# =============================================================================
class RESMAEngine(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.lattice = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.GELU(),
            nn.Linear(256, 64)
        )
        self.ricci_metric = nn.Linear(64, 32)
        self.output = nn.Linear(32, 1)

    def forward(self, x):
        z = self.lattice(x)
        curvature = torch.tanh(self.ricci_metric(z))
        energy = torch.norm(curvature, p=2, dim=1, keepdim=True)
        return torch.sigmoid(self.output(curvature) + 0.1 * energy), energy

# =============================================================================
# 2. INTEGRATION INTO YOUR REPORTING SYSTEM
# =============================================================================

def apply_resma_intelligence(df):
    """
    Inyecta la IA RESMA en el flujo de datos de LazyOwn.
    Aprende de tus reglas y descubre lo que ellas no ven.
    """
    print("\n[*] Entrenando Motor de Inteligencia RESMA 5.2...")

    # Feature Engineering (Usando tus columnas)
    df['full_payload'] = df['command'].astype(str) + " " + df['args'].fillna('').astype(str)

    vectorizer = TfidfVectorizer(max_features=512, ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(df['full_payload']).toarray()
    X_tensor = torch.tensor(X_vec, dtype=torch.float32)

    # Ground Truth basado en TUS reglas
    y_reglas = (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']).astype(float)
    y_tensor = torch.tensor(y_reglas.values, dtype=torch.float32).reshape(-1, 1)

    model = RESMAEngine(X_vec.shape[1])
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    # Fast training to capture the 'shape' of your attacks
    model.train()
    for _ in range(40):
        optimizer.zero_grad()
        probs, _ = model(X_tensor)
        loss = F.binary_cross_entropy(probs, y_tensor)
        loss.backward()
        optimizer.step()

    # Inferencia: Buscando Amenazas Sombra
    model.eval()
    with torch.no_grad():
        final_probs, energy = model(X_tensor)
        df['ia_risk_score'] = final_probs.numpy()
        df['ia_energy'] = energy.numpy()

    # Geometric anomaly threshold (97th percentile)
    threshold = np.percentile(df['ia_energy'], 97)
    df['is_shadow_threat'] = ((df['ia_energy'] > threshold) & (y_reglas == 0)).astype(int)

    return df

# =============================================================================
# 3. REPORTE FINAL (RESUMEN DE INTELIGENCIA)
# =============================================================================

def final_resma_report(df):
    shadows = df[df['is_shadow_threat'] == 1]

    print("\n" + "="*60)
    print("RESMA 5.2 THREAT ANALYSIS")
    print("="*60)
    print(f"Total Events:             {len(df)}")
    print(f"Detected by Rules:        {int((df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']).sum())}")
    print(f"Shadow Threats (AI):      {len(shadows)}")

    if len(shadows) > 0:
        print("\n[!] SHADOW DISCOVERIES (High Structural Energy):")
        for _, row in shadows.sort_values('ia_energy', ascending=False).head(5).iterrows():
            print(f"  • {row['command']} {row['args'][:60]}... (Energy: {row['ia_energy']:.4f})")

    return len(shadows)

# =============================================================================
# FLUJO PRINCIPAL
# =============================================================================

# This is where the script actually runs
def lol():
    filepath = "sessions/LazyOwn_session_report.csv"

    if os.path.exists(filepath):
        # 1. Load and clean (as you do)
        df = pd.read_csv(filepath, on_bad_lines='skip')

        # Simulate your flags so the code works standalone
        # En tu script real, estas columnas ya existen
        df['is_dangerous'] = df['args'].str.contains('rm -rf|export', na=False)
        df['is_c2_or_postexploit'] = df['args'].str.contains('nc |powershell', na=False)
        df['contains_creds'] = df['args'].str.contains(':', na=False)

        # 2. Inyectar inteligencia
        df = apply_resma_intelligence(df)

        # 3. Mostrar reporte
        final_resma_report(df)
    else:
        print(f"File not found: {filepath}")

# Style configuration
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
sns.set(font_scale=1.1)

# Directorios
OUTPUT_DIR = Path("sessions/reports")
STATIC = Path("static")
AI_MODEL_DIR = Path("sessions/ai_model")
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC.mkdir(exist_ok=True)
AI_MODEL_DIR.mkdir(exist_ok=True)

# Command categories (expanded)
COMMAND_CATEGORIES = {
    'nmap': 'recon', 'gobuster': 'recon', 'dirb': 'recon', 'nikto': 'recon',
    'sqlmap': 'exploit', 'hydra': 'brute_force', 'john': 'brute_force',
    'hashcat': 'brute_force', 'echo': 'data_write', 'searchsploit': 'exploit_research',
    'sudo': 'privilege_escalation', 'msfconsole': 'exploit', 'msfvenom': 'payload_creation',
    'cp': 'file_transfer', 'mv': 'file_transfer', 'wget': 'download',
    'curl': 'download', 'nc': 'network', 'netcat': 'network', 'ssh': 'remote_access',
    'telnet': 'remote_access', 'ftp': 'remote_access', 'smbclient': 'remote_access',
    'git': 'recon', 'whois': 'recon', 'dig': 'recon', 'nslookup': 'recon',
    'upx': 'packer', 'python3': 'scripting', 'python': 'scripting', 'perl': 'scripting',
    'powershell': 'execution', 'cmd': 'execution', 'cmd.exe': 'execution',
    'certutil': 'download', 'bitsadmin': 'download', 'regsvr32': 'lolbin',
    'rundll32': 'lolbin', 'wmic': 'lolbin', 'schtasks': 'persistence',
    'at': 'persistence', 'sc': 'persistence', 'psexec': 'lateral_movement',
    'evil-winrm': 'remote_access', 'crackmapexec': 'lateral_movement'
}

# [~] Palabras clave de comandos peligrosos
DANGEROUS_KEYWORDS = [
    'rm -rf', 'chmod 777', 'mkfs', 'dd if=', 'format', 'delete', 'del ',
    'rmdir', 'shutdown', 'poweroff', 'iptables -F'
]

# C2 and post-exploitation patterns
C2_INDICATORS = [
    r'bash -i.*>& /dev/tcp',  # Reverse shell
    r'nc .* -e',              # Netcat reverse shell
    r'powershell.*-Enc',      # PowerShell encoded
    r'certutil.*-decode',     # Certutil como downloader
    r'bitsadmin.*Transfer',   # BitsAdmin C2
    r'Invoke-WebRequest',     # PowerShell download
    r'wget.*http.*\.exe',     # Descarga de binarios
    r'curl.*http.*\.dll',
    r'python.*-m http',       # Quick HTTP server
    r'echo.*base64.*\|.*bash' # Obfuscated payloads
]

def train_ai_model(df):
    """Entrena un modelo desde cero con todos los detalles de entrenamiento"""
    print("\n" + "="*60)
    print("TRAINING AI MODEL FROM SCRATCH")
    print("="*60)

    # Create combined label
    df['es_malicioso'] = (
        df['is_c2_or_postexploit'] |
        df['is_dangerous'] |
        df['contains_creds']
    ).astype(int)

    # Filter valid data
    df_text = df.dropna(subset=['command', 'args']).copy()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)

    X = df_text['texto']
    y = df_text['es_malicioso']

    print(f"Training data: {len(X)} commands ({y.sum()} malicious, {len(y) - y.sum()} benign)")

    if y.sum() == 0:
        print("No malicious examples. Cannot train.")
        return None, None

    # Vectorization
    print("\nVectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        lowercase=True,
        token_pattern=r'(?u)\b\w+\b'
    )
    X_vec = vectorizer.fit_transform(X)

    # Train/test split
    print("Splitting train/test (80%/20%)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42, stratify=y
    )
    # FIX: Use .shape[0] instead of len() for sparse matrices
    print(f"   - Training: {X_train.shape[0]} commands")
    print(f"   - Test: {X_test.shape[0]} commands")

    # Training
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    print("\nMODEL EVALUATION")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.2%}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Malicious']))

    # Guardar modelo
    joblib.dump(model, AI_MODEL_DIR / "malicious_command_model.pkl")
    joblib.dump(vectorizer, AI_MODEL_DIR / "tfidf_vectorizer.pkl")
    print(f"Model saved to: {AI_MODEL_DIR}/")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Benign','Malicious'], yticklabels=['Benign','Malicious'])
    plt.title("Confusion Matrix - Malicious Command Detection")
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150, bbox_inches='tight')
    plt.close()

    return model, vectorizer


def load_or_train_model(df):
    """Carga modelo existente o entrena uno nuevo, y lo actualiza con nuevos datos"""
    model_path = AI_MODEL_DIR / "malicious_command_model.pkl"
    vectorizer_path = AI_MODEL_DIR / "tfidf_vectorizer.pkl"

    df['es_malicioso'] = (
        df['is_c2_or_postexploit'] |
        df['is_dangerous'] |
        df['contains_creds']
    ).astype(int)
    df_text = df.dropna(subset=['command', 'args']).copy()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)
    X_text = df_text['texto']
    y_true = df_text['es_malicioso']

    if model_path.exists() and vectorizer_path.exists():
        print("Loading previous model...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        try:
            X_vec = vectorizer.transform(X_text)
            print(f"Retraining with {len(X_text)} new commands...")
            model.fit(X_vec, y_true)
            joblib.dump(model, model_path)
            print("Model updated and saved.")
        except Exception as e:
            print(f"Error adjusting model: {e}. Retraining from scratch.")
            return train_ai_model(df)
    else:
        print("Model not found. Training from scratch...")
        return train_ai_model(df)

    return model, vectorizer

def apply_ai_predictions(df, model, vectorizer):
    """Aplica predicciones del modelo al DataFrame"""
    df_text = df[['command', 'args']].copy().dropna()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)
    X_vec = vectorizer.transform(df_text['texto'])

    df_text['ia_malicious_score'] = model.predict_proba(X_vec)[:, 1]
    df_text['ia_prediccion'] = model.predict(X_vec)

    df = df.join(df_text[['ia_malicious_score', 'ia_prediccion']])
    df['ia_malicious_score'].fillna(0.0, inplace=True)
    df['ia_prediccion'].fillna(0, inplace=True)
    return df

def analyze_ia_vs_rules(df):
    """Analiza discrepancias entre reglas y modelo IA"""
    print("\n" + "="*60)
    print("COMPARATIVE ANALYSIS: RULES VS AI")
    print("="*60)

    regla_mal = (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds'])
    ia_mal = df['ia_prediccion'].astype(bool)

    nuevos_ia = df[~regla_mal & ia_mal]  # AI detects, rules do not
    fallo_ia = df[regla_mal & ~ia_mal]  # Rules detect, AI does not

    print(f"Malicious commands (rules): {regla_mal.sum()}")
    print(f"Malicious commands (AI): {ia_mal.sum()}")
    print(f"New findings (AI detected, rules missed): {len(nuevos_ia)}")
    print(f"False negatives (rules detected, AI missed): {len(fallo_ia)}")

    if len(nuevos_ia) > 0:
        print("\nNEW AI FINDINGS:")
        for _, row in nuevos_ia.head(5).iterrows():
            print(f"  [{row['domain']}] {row['command']} {row['args']} (score: {row['ia_malicious_score']:.3f})")

    if len(fallo_ia) > 0:
        print("\nCASES WHERE AI MISSED:")
        for _, row in fallo_ia.head(5).iterrows():
            print(f"  [{row['domain']}] {row['command']} {row['args']}")

    return {
        "reglas_maliciosos": int(regla_mal.sum()),
        "ia_maliciosos": int(ia_mal.sum()),
        "new_ai_findings": len(nuevos_ia),
        "ai_false_negatives": len(fallo_ia)
    }
def load_and_clean_data_robust(filepath):
    """Cargar y limpiar los datos de forma robusta"""
    print("Loading data in a robust way...")

    try:
        df = pd.read_csv(filepath, on_bad_lines='skip')
    except Exception:
        df = parse_csv_manual(filepath)

    if df.empty:
        print("No data loaded.")
        return df

    print(f"Data loaded: {len(df)} records")

    expected_columns = ['start','end','source_ip','source_port','destination_ip',
                       'destination_port','domain','subdomain','url','pivot_port',
                       'command','args']

    if len(df.columns) != len(expected_columns):
        df = df.reindex(columns=expected_columns, fill_value='')

    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['end'] = pd.to_datetime(df['end'], errors='coerce')
    df = df.dropna(subset=['start', 'end'])

    df['duration'] = (df['end'] - df['start']).dt.total_seconds()
    df['hour'] = df['start'].dt.hour
    df['day_of_week'] = df['start'].dt.day_name()
    df['date'] = df['start'].dt.date

    df['command_length'] = df['command'].astype(str).str.len()
    df['args_length'] = df['args'].astype(str).str.len()

    df['contains_creds'] = df['args'].str.contains(":", na=False) & df['args'].str.contains(">", na=False)
    df['is_dangerous'] = df['args'].apply(lambda x: any(kw in str(x) for kw in DANGEROUS_KEYWORDS))
    df['command_category'] = df['command'].apply(lambda c: COMMAND_CATEGORIES.get(str(c).lower(), 'other'))
    df['is_c2_or_postexploit'] = df['args'].apply(lambda x: any(re.search(pat, str(x), re.IGNORECASE) for pat in C2_INDICATORS))

    print(f"Data processed: {len(df)} valid records")
    return df

def parse_csv_manual(filepath):
    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        header = lines[0].strip().split(',')
        for line in lines[1:]:
            try:
                reader = csv.reader(io.StringIO(line.strip()), delimiter=',', quotechar='"')
                row = next(reader)
                if len(row) < len(header):
                    row += [''] * (len(header) - len(row))
                elif len(row) > len(header):
                    row = row[:len(header)-1] + [','.join(row[len(header)-1:])]
                if len(row) == len(header):
                    rows.append(row)
            except Exception:
                continue
        return pd.DataFrame(rows, columns=header) if rows else pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def executive_kpis(df):
    total = len(df)
    suspicious = len(df[df['is_c2_or_postexploit']])
    dangerous = len(df[df['is_dangerous']])
    creds = len(df[df['contains_creds']])
    unique_domains = df['domain'].nunique()
    active_days = (df['start'].max() - df['start'].min()).days + 1

    kpis = {
        "Total Red Team Activity": total,
        "Suspicious Commands (C2/Post-Exploit)": suspicious,
        "Suspicious Activity Rate (%)": f"{(suspicious / total * 100):.2f}%",
        "Dangerous Commands": dangerous,
        "Exposed Credentials": creds,
        "Compromised Domains": unique_domains,
        "Campaign Duration (days)": active_days,
        "Commands per Day (avg)": f"{total / active_days:.1f}"
    }

    print("\n" + "="*60)
    print("EXECUTIVE SECURITY KPIs")
    print("="*60)
    for k, v in kpis.items():
        print(f"  • {k:<35} : {v}")

    return kpis

def strategic_okrs(df, kpis):
    okrs = {
        "OKR 1: Reduce credential exposure": {
            "Objective": "Eliminate plaintext credential writes",
            "Goal": "0 commands writing credentials with 'echo'",
            "Current": kpis["Exposed Credentials"],
            "Status": "Critical" if kpis["Exposed Credentials"] > 0 else "Achieved"
        },
        "OKR 2: Prevent post-exploitation": {
            "Objective": "Detection and blocking of C2 techniques",
            "Goal": "0 obfuscated or reverse shell commands",
            "Current": kpis["Suspicious Commands (C2/Post-Exploit)"],
            "Status": "Critical" if kpis["Suspicious Commands (C2/Post-Exploit)"] > 0 else "Achieved"
        },
        "OKR 3: Strengthen security posture": {
            "Objective": "Reduce use of dangerous commands",
            "Goal": "Less than 1% dangerous commands",
            "Current": f"{(kpis['Dangerous Commands'] / kpis['Total Red Team Activity'] * 100):.2f}%",
            "Status": "Warning" if kpis["Dangerous Commands"] > 0 else "Achieved"
        }
    }

    print("\n" + "="*60)
    print("STRATEGIC SECURITY OKRs")
    print("="*60)
    for okr, data in okrs.items():
        print(f"{okr}")
        for k, v in data.items():
            print(f"   • {k}: {v}")
        print()

    return okrs

def generate_visualizations(df, kpis):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    cat_counts = df['command_category'].value_counts().head(8)
    axes[0,0].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%')
    axes[0,0].set_title("Distribution by Command Category")

    hourly = df['hour'].value_counts().sort_index()
    axes[0,1].bar(hourly.index, hourly.values, color='skyblue')
    axes[0,1].set_title("Activity by Hour of Day")
    axes[0,1].set_xlabel("Hour")
    axes[0,1].set_ylabel("Command Count")

    top_domains = df['domain'].value_counts().head(6)
    axes[1,0].barh(top_domains.index, top_domains.values, color='coral')
    axes[1,0].set_title("Top Targeted Domains")
    axes[1,0].set_xlabel("Command Count")

    risks = [
        kpis["Suspicious Commands (C2/Post-Exploit)"],
        kpis["Dangerous Commands"],
        kpis["Exposed Credentials"]
    ]
    axes[1,1].bar(["C2/Post-Exploit", "Dangerous", "Credentials"], risks, color=['red', 'orange', 'purple'])
    axes[1,1].set_title("Risk Indicators")
    axes[1,1].set_ylabel("Count")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "security_dashboard.png", dpi=150, bbox_inches='tight')
    plt.savefig(STATIC / "security_dashboard.png", dpi=150, bbox_inches='tight')
    print(f"Chart saved: {OUTPUT_DIR}/security_dashboard.png")

def export_report(df, kpis, okrs, ia_analysis):
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "kpis": kpis,
            "okrs": okrs,
            "ia_analysis": ia_analysis
        },
        "detailed_analysis": {
            "basic_statistics": {
                "total_records": len(df),
                "unique_commands": df['command'].nunique(),
                "unique_source_ips": df['source_ip'].nunique(),
                "unique_domains": df['domain'].nunique(),
                "active_days": (df['start'].max() - df['start'].min()).days + 1
            },
            "ia_detection_stats": {
                "total_malicious_predicted": int(df['ia_prediccion'].sum()),
                "high_risk_commands": int((df['ia_malicious_score'] > 0.8).sum()),
                "new_ai_findings": ia_analysis["new_ai_findings"],
                "ai_false_negatives": ia_analysis["ai_false_negatives"]
            },
            "top_commands": df['command'].value_counts().head(10).to_dict(),
            "exposed_credentials": df[df['contains_creds']].head(10)[['command','args','domain','start']].to_dict('records'),
            "c2_commands": df[df['is_c2_or_postexploit']].head(10)[['command','args','domain','start']].to_dict('records'),
            "new_ai_findings": df[
                ~(df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']) &
                (df['ia_prediccion'] == 1)
            ].head(10)[['command','args','domain','ia_malicious_score']].to_dict('records'),
            "ai_false_negatives": df[
                (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']) &
                (df['ia_prediccion'] == 0)
            ].head(10)[['command','args','domain']].to_dict('records')
        }
    }

    output_path = OUTPUT_DIR / "executive_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"JSON report exported: {output_path}")
    import subprocess
    import shutil
    if shutil.which("gum"):
        subprocess.run(
            f"python3 modules/vuln_bot_cli.py --file {output_path} --provider groq --mode console | gum format",
            shell=True
        )
    else:
        subprocess.run(
            ["python3", "modules/vuln_bot_cli.py", "--file", output_path, "--provider", "groq", "--mode", "console"]
        )



# Analysis functions (kept as-is)
def basic_statistics(df):
    print("\nBASIC STATISTICS")
    print("-"*60)
    print(f"Total records: {len(df):,}")
    print(f"Total unique commands: {df['command'].nunique():,}")
    print(f"Total unique source IPs: {df['source_ip'].nunique():,}")
    print(f"Total unique domains: {df['domain'].nunique():,}")
    try:
        print(f"Data period: {df['start'].min()} to {df['start'].max()}")
        print(f"Days of activity: {(df['start'].max() - df['start'].min()).days}")
    except Exception:
        print("Could not calculate dates")

def command_analysis(df):
    print("\nCOMMAND ANALYSIS")
    print("-"*60)
    top_commands = df['command'].value_counts().head(15)
    print("Top 15 most used commands:")
    for i, (cmd, count) in enumerate(top_commands.items(), 1):
        print(f"  {i:2d}. {cmd:<20} ({count:,} times)")
    categories = df['command_category'].value_counts()
    print("\nDistribution by category:")
    for cat, count in categories.items():
        percentage = (count / len(df)) * 100
        print(f"  {cat:<20} {count:,} ({percentage:.1f}%)")

def network_analysis(df):
    print("\nNETWORK ANALYSIS")
    print("-"*60)
    top_ips = df['source_ip'].value_counts().head(10)
    print("Top 10 most active source IPs:")
    for ip, count in top_ips.items():
        print(f"  {ip:<15} ({count:,} commands)")
    top_domains = df['domain'].value_counts().head(10)
    print("\nTop 10 most frequent domains:")
    for domain, count in top_domains.items():
        print(f"  {domain:<30} ({count:,} commands)")

def temporal_analysis(df):
    print("\nTEMPORAL ANALYSIS")
    print("-"*60)
    hourly_activity = df['hour'].value_counts().sort_index()
    print("Activity distribution by hour:")
    for hour, count in hourly_activity.items():
        print(f"  {hour:02d}:00 - {hour:02d}:59  {count:,} commands")

def statistical_analysis(df):
    print("\nSTATISTICAL ANALYSIS")
    print("-"*60)
    duration_stats = df['duration'].describe()
    print("Command duration statistics (seconds):")
    for stat, value in duration_stats.items():
        print(f"  {stat:<10} {value:.4f}")

def security_insights(df):
    print("\nSECURITY INSIGHTS")
    print("-"*60)
    creds_df = df[df['contains_creds']]
    if len(creds_df) > 0:
        print("CREDENTIALS FOUND:")
        sample_creds = creds_df[['command', 'args', 'domain']].head(5)
        for _, row in sample_creds.iterrows():
            print(f"  Command: {row['command']}")
            print(f"  Args: {row['args']}")
            print(f"  Domain: {row['domain']}")
            print("  " + "-"*50)
    danger_df = df[df['is_dangerous']]
    if len(danger_df) > 0:
        print(f"\nDANGEROUS COMMANDS ({len(danger_df)} found):")
        danger_sample = danger_df[['command', 'args', 'domain']].head(5)
        for _, row in danger_sample.iterrows():
            print(f"  Command: {row['command']}")
            print(f"  Args: {row['args']}")
            print(f"  Domain: {row['domain']}")
            print("  " + "-"*50)

def main():
    filepath = "sessions/LazyOwn_session_report.csv"
    print(f"Analyzing: {filepath}")

    if not os.path.exists(filepath):
        print("ERROR: CSV file not found.")
        return

    df = load_and_clean_data_robust(filepath)
    if df.empty:
        return

    # --- IA: Cargar o reentrenar modelo ---
    model, vectorizer = load_or_train_model(df)
    if model is None or vectorizer is None:
        print("Could not load or train model. Continuing without AI...")
        return

    # --- Apply predictions ---
    df = apply_ai_predictions(df, model, vectorizer)

    # --- Technical analysis ---
    print("\n" + "="*60)
    print("DETAILED TECHNICAL ANALYSIS")
    print("="*60)
    basic_statistics(df)
    command_analysis(df)
    network_analysis(df)
    temporal_analysis(df)
    statistical_analysis(df)
    security_insights(df)

    # --- Comparativa IA vs Reglas ---
    ia_analysis = analyze_ia_vs_rules(df)

    # --- KPIs y OKRs ---
    kpis = executive_kpis(df)
    okrs = strategic_okrs(df, kpis)
    generate_visualizations(df, kpis)
    export_report(df, kpis, okrs, ia_analysis)

    print("\n" + "="*60)
    print("SECURITY REPORT COMPLETED")
    print("="*60)
    print(f"Artifacts generated in: ./{OUTPUT_DIR}/")
    print("   • security_dashboard.png")
    print("   • confusion_matrix.png")
    print("   • executive_report.json")
    lol()
if __name__ == "__main__":
    main()


def generate_security_report(csv_path: str | None = None, output_dir: str | None = None) -> dict:
    """Generate a security intelligence report from a LazyOwn session CSV.

    This is the framework integration entry point for ``report.py``.
    Can be called from the CLI, MCP tools, or the autonomous loop.

    Args:
        csv_path: Path to the session CSV file. Defaults to
            ``sessions/LazyOwn_session_report.csv``.
        output_dir: Directory for report artifacts. Defaults to
            ``sessions/report_ai/``.

    Returns:
        Dict with ``status``, ``csv_path``, ``output_dir``, ``kpis``,
        and ``error`` keys.
    """
    try:
        _csv_path = Path(csv_path) if csv_path else Path("sessions/LazyOwn_session_report.csv")
        _output_dir = Path(output_dir) if output_dir else _csv_path.parent / "report_ai"
        _output_dir.mkdir(parents=True, exist_ok=True)

        if not _csv_path.exists():
            return {"status": "error", "error": f"CSV not found: {_csv_path}", "csv_path": str(_csv_path)}

        global OUTPUT_DIR
        OUTPUT_DIR = str(_output_dir)

        df = load_and_clean_data_robust(str(_csv_path))
        if df.empty:
            return {"status": "error", "error": "Empty dataset after cleaning", "csv_path": str(_csv_path)}

        model, vectorizer = load_or_train_model(df)
        if model is None or vectorizer is None:
            return {"status": "error", "error": "Model training failed", "csv_path": str(_csv_path)}

        df = apply_ai_predictions(df, model, vectorizer)
        kpis = executive_kpis(df)
        okrs = strategic_okrs(df, kpis)
        ia_analysis = analyze_ia_vs_rules(df)
        generate_visualizations(df, kpis)
        export_report(df, kpis, okrs, ia_analysis)

        return {
            "status": "ok",
            "csv_path": str(_csv_path),
            "output_dir": str(_output_dir),
            "kpis": kpis,
            "okrs": okrs,
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc), "csv_path": str(csv_path) if csv_path else ""}
