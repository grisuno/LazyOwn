const DEFAULT_ENDPOINT = "http://127.0.0.1:8898/__lazyown/sync";
const statusEl = document.getElementById("status");

async function loadConfig() {
  const stored = await chrome.storage.local.get(["endpoint", "token", "interval", "domainFilter", "lastResult"]);
  document.getElementById("endpoint").value = stored.endpoint || DEFAULT_ENDPOINT;
  document.getElementById("token").value = stored.token || "";
  document.getElementById("interval").value = stored.interval && Number(stored.interval) > 0 ? Number(stored.interval) : 15;
  document.getElementById("domainFilter").value = stored.domainFilter || "";
  renderResult(stored.lastResult);
}

function renderResult(result) {
  if (!result) {
    statusEl.textContent = "";
    return;
  }
  if (result.ok) {
    statusEl.textContent = `synced: ${result.cookies} cookies`;
    statusEl.style.color = "#7ef29d";
  } else {
    statusEl.textContent = `error: ${result.error}`;
    statusEl.style.color = "#f07d7d";
  }
}

document.getElementById("save").addEventListener("click", async () => {
  const endpoint = document.getElementById("endpoint").value.trim() || DEFAULT_ENDPOINT;
  const token = document.getElementById("token").value.trim();
  const interval = Math.max(1, Number(document.getElementById("interval").value) || 15);
  const domainFilter = document.getElementById("domainFilter").value.trim();
  await chrome.storage.local.set({ endpoint, token, interval, domainFilter });
  await chrome.runtime.sendMessage({ type: "configChanged" });
  statusEl.textContent = "saved";
  statusEl.style.color = "#7ef29d";
});

document.getElementById("sync").addEventListener("click", async () => {
  statusEl.textContent = "syncing...";
  statusEl.style.color = "#999";
  const result = await chrome.runtime.sendMessage({ type: "sync" });
  renderResult(result);
});

loadConfig();
