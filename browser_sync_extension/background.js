const DEFAULT_ENDPOINT = "http://127.0.0.1:8898/__lazyown/sync";
const DEFAULT_INTERVAL_MIN = 15;
const TAB_SYNC_MIN_GAP_MS = 60000;
const MAX_COOKIES = 8000;

let lastTabSync = 0;

async function config() {
  const stored = await chrome.storage.local.get(["endpoint", "token", "interval", "domainFilter"]);
  return {
    endpoint: stored.endpoint || DEFAULT_ENDPOINT,
    token: stored.token || "",
    interval: Number(stored.interval) > 0 ? Number(stored.interval) : DEFAULT_INTERVAL_MIN,
    domainFilter: (stored.domainFilter || "").trim(),
  };
}

function domainAllowed(domain, filter) {
  if (!filter) {
    return true;
  }
  const target = String(domain || "").toLowerCase().replace(/^\./, "");
  return filter
    .split(",")
    .map((entry) => entry.trim().toLowerCase().replace(/^\./, ""))
    .filter(Boolean)
    .some((entry) => target === entry || target.endsWith("." + entry));
}

async function highEntropyHints() {
  const hints = {};
  try {
    if (navigator.userAgentData) {
      const high = await navigator.userAgentData.getHighEntropyValues([
        "platform",
        "platformVersion",
        "architecture",
        "bitness",
        "model",
        "uaFullVersion",
        "fullVersionList",
      ]);
      const brands = high.fullVersionList || navigator.userAgentData.brands || [];
      if (brands.length) {
        const list = brands
          .map((b) => `"${b.brand.replace(/"/g, "")}";v="${b.version}"`)
          .join(", ");
        hints["Sec-CH-UA"] = list;
        hints["Sec-CH-UA-Mobile"] = navigator.userAgentData.mobile ? "?1" : "?0";
      }
      if (high.platform) {
        hints["Sec-CH-UA-Platform"] = `"${high.platform.replace(/"/g, "")}"`;
      }
      if (high.uaFullVersion) {
        hints["Sec-CH-UA-Full-Version"] = `"${high.uaFullVersion.replace(/"/g, "")}"`;
      }
    }
  } catch (err) {
    hints._error = String(err);
  }
  return hints;
}

function sanitizeHeader(value) {
  return String(value ?? "").replace(/[\r\n\x00]/g, "");
}

async function collectProfile(filter) {
  const all = await chrome.cookies.getAll({});
  const cookies = filter ? all.filter((c) => domainAllowed(c.domain, filter)) : all;
  const hints = await highEntropyHints();
  return {
    synced_at_client: Date.now(),
    user_agent: sanitizeHeader(navigator.userAgent),
    languages: Array.from(navigator.languages || []).map(sanitizeHeader),
    client_hints: Object.fromEntries(
      Object.entries(hints).map(([k, v]) => [k, sanitizeHeader(v)])
    ),
    cookies: cookies.slice(0, MAX_COOKIES).map((c) => ({
      domain: c.domain,
      name: c.name,
      value: c.value,
      path: c.path,
      secure: c.secure,
      httpOnly: c.httpOnly,
      hostOnly: c.hostOnly,
      session: c.session,
      sameSite: c.sameSite,
      expirationDate: c.expirationDate,
    })),
  };
}

async function syncNow() {
  const cfg = await config();
  if (!cfg.token) {
    return { ok: false, error: "token not configured (open the popup and paste the LazyOwn token)" };
  }
  let profile;
  try {
    profile = await collectProfile(cfg.domainFilter);
  } catch (err) {
    return { ok: false, error: String(err) };
  }
  try {
    const response = await fetch(cfg.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-LazyOwn-Token": cfg.token },
      body: JSON.stringify(profile),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      return { ok: false, error: `HTTP ${response.status}: ${data.error || response.statusText}` };
    }
    const result = { ok: true, cookies: data.cookies ?? 0, at: Date.now() };
    await chrome.storage.local.set({ lastResult: result });
    return result;
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

async function armAlarm() {
  const cfg = await config();
  await chrome.alarms.clear("lazysync");
  await chrome.alarms.create("lazysync", { periodInMinutes: cfg.interval });
}

chrome.runtime.onInstalled.addListener(async () => {
  await armAlarm();
  await syncNow();
});

chrome.runtime.onStartup.addListener(async () => {
  await syncNow();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "lazysync") {
    syncNow();
  }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab && /^https?:/i.test(tab.url || "")) {
    const now = Date.now();
    if (now - lastTabSync >= TAB_SYNC_MIN_GAP_MS) {
      lastTabSync = now;
      syncNow();
    }
  }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "sync") {
    syncNow().then((result) => sendResponse(result));
    return true;
  }
  if (msg && msg.type === "configChanged") {
    armAlarm().then(() => sendResponse({ ok: true }));
    return true;
  }
  sendResponse({ ok: false, error: "unknown message" });
  return false;
});
