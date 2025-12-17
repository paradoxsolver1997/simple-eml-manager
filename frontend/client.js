const updateBtn = document.getElementById("update-btn");
const cancelBtn = document.getElementById("cancel-btn");

const statusBox = document.getElementById("update-status");
const statusText = document.getElementById("status-text");
const progressBar = document.getElementById("status-progress");

// you hope to be in update period disable All controls of
const controlsToDisable = [
document.getElementById("update-btn"),
document.getElementById("search-input"),
document.getElementById("search-btn"),
].filter(Boolean);

let pollTimer = null;

/* ----------------------------
* UI Helper function
* ---------------------------- */

function disableControls() {
controlsToDisable.forEach(el => el.disabled = true);
}

function enableControls() {
controlsToDisable.forEach(el => el.disabled = false);
}

function showStatus() {
statusBox.style.display = "block";
}

function hideStatus() {
statusBox.style.display = "none";
}

function updateProgress(current, total, message) {
if (total > 0) {
    const percent = Math.floor((current / total) * 100);
    progressBar.value = percent;
    statusText.textContent = `${message} (${current}/${total})`;
} else {
    progressBar.value = 0;
    statusText.textContent = message || "Working...";
}
}

function resetProgress() {
  progressBar.value = 0;
  statusText.textContent = "";
}

async function search() {
  const q = document.getElementById("query").value;
  const field = document.getElementById("field").value;

  const res = await fetch(
    `/api/search?q=${encodeURIComponent(q)}&field=${field}`
  );

  const data = await res.json();
  const results = document.getElementById("results");
  results.innerHTML = "";

  data.results.forEach(item => {
  const li = document.createElement("li");
  li.className = "result-item";
  li.innerHTML = `
    <div class="result-subject">${escapeHtml(item.subject)}</div>

    <div class="result-meta">
      <span>From: ${escapeHtml(item.sender)}</span>
      <span>To: ${escapeHtml(item.recipients)}</span>
    </div>

    <div class="result-preview">
      ${escapeHtml(item.body.slice(0, 200))}
    </div>
  `;

    li.addEventListener("click", async () => {
        const existing = li.querySelector(".result-body");

        // —— Expanded → fold ——
        if (existing) {
            existing.remove();
            return;
        }

        // —— Not expanded → Load and expand ——
        try {
            const resp = await fetch(
            `/api/email?path=${encodeURIComponent(item.path)}`
            );

            if (!resp.ok) {
            throw new Error("Failed to load email");
            }

            const email = await resp.json();

            const bodyDiv = document.createElement("div");
            bodyDiv.className = "result-body";
            bodyDiv.textContent = email.body || "(empty body)";

            li.appendChild(bodyDiv);
        } catch (err) {
            console.error(err);
            alert("Failed to load email content");
        }
    });


  results.appendChild(li);
});

}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


/* ----------------------------
* rear end API call
* ---------------------------- */

async function startUpdate() {
const resp = await fetch("/api/update_library", {
    method: "POST",
});
return resp.json();
}

async function fetchStatus() {
const resp = await fetch("/api/update_status");
return resp.json();
}

async function cancelUpdate() {
await fetch("/api/update_cancel", {
    method: "POST",
});
}

/* ----------------------------
* Polling logic
* ---------------------------- */

function startPolling() {
pollTimer = setInterval(async () => {
    try {
    const status = await fetchStatus();

    if (status.status === "running") {
        updateProgress(
        status.current,
        status.total,
        status.message || "Updating"
        );
        return;
    }

    // finished / cancelled / error
    stopPolling();

    if (status.status === "finished") {
        updateProgress(status.total, status.total, "Completed");
    } else if (status.status === "cancelled") {
        statusText.textContent = "Cancelled";
    } else if (status.status === "error") {
        statusText.textContent = "Error: " + (status.error || "Unknown error");
    }

    setTimeout(() => {
        hideStatus();
        resetProgress();
        enableControls();
    }, 1000);

    } catch (err) {
    console.error("Polling error:", err);
    stopPolling();
    enableControls();
    }
}, 500);
}

function stopPolling() {
if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
}
}

/* ----------------------------
* event binding
* ---------------------------- */

updateBtn.addEventListener("click", async () => {
disableControls();
showStatus();
resetProgress();
statusText.textContent = "Starting update...";

try {
    const result = await startUpdate();
    if (!result.ok) {
    throw new Error(result.message || "Failed to start update");
    }
    startPolling();
} catch (err) {
    console.error(err);
    statusText.textContent = "Failed to start update";
    enableControls();
}
});

cancelBtn.addEventListener("click", async () => {
cancelBtn.disabled = true;
statusText.textContent = "Cancelling...";
try {
    await cancelUpdate();
} finally {
    cancelBtn.disabled = false;
}
});