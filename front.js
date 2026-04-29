const API = "http://127.0.0.1:5000";

let sessionToken = localStorage.getItem("ripple_token") || null;
let currentUser  = localStorage.getItem("ripple_user")  || null;

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${sessionToken}`
    };
}

function saveSession(token, username) {
    sessionToken = token;
    currentUser  = username;
    localStorage.setItem("ripple_token", token);
    localStorage.setItem("ripple_user",  username);
}

function clearSession() {
    sessionToken = null;
    currentUser  = null;
    localStorage.removeItem("ripple_token");
    localStorage.removeItem("ripple_user");
}

function showPage(id) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

function showTab(tab) {
    document.getElementById("formLogin").style.display  = tab === "login"  ? "" : "none";
    document.getElementById("formSignup").style.display = tab === "signup" ? "" : "none";
    document.getElementById("tabLogin").classList.toggle("active",  tab === "login");
    document.getElementById("tabSignup").classList.toggle("active", tab === "signup");
    clearAuthMessages();
}

function clearAuthMessages() {
    ["loginError","loginInfo","signupError","signupInfo"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = "";
    });
}

async function signup() {
    const username = document.getElementById("signupUsername").value.trim();
    const errEl    = document.getElementById("signupError");
    const infoEl   = document.getElementById("signupInfo");
    errEl.textContent = "";
    infoEl.textContent = "";

    if (!username) { errEl.textContent = "Enter your Minecraft username."; return; }

    try {
        const res  = await fetch(`${API}/api/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username })
        });
        const data = await res.json();
        if (data.error) { errEl.textContent = data.error; return; }
        infoEl.textContent = "Account created! Switch to Login to continue.";
        document.getElementById("signupUsername").value = "";
    } catch (e) {
        errEl.textContent = "Could not reach server.";
    }
}

async function requestCode() {
    const username = document.getElementById("loginUsername").value.trim();
    const errEl    = document.getElementById("loginError");
    const infoEl   = document.getElementById("loginInfo");
    errEl.textContent  = "";
    infoEl.textContent = "";

    if (!username) { errEl.textContent = "Enter your Minecraft username."; return; }

    try {
        const res  = await fetch(`${API}/api/request-code`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username })
        });
        const data = await res.json();
        if (data.error) { errEl.textContent = data.error; return; }

        document.getElementById("loginCodeSection").style.display = "";
        infoEl.textContent = "Code sent! Check your terminal (dev) or in-game DM.";

        // Dev convenience: auto-fill the code from the server response
        if (data.dev_code) {
            document.getElementById("loginCode").value = data.dev_code;
            infoEl.textContent = `Dev mode — code auto-filled: ${data.dev_code}`;
            document.querySelector(".code-hint").innerHTML =
                `Type <code>/msg evn3 ${data.dev_code}</code> in-game — or use the dev code auto-filled below.`;
        }
    } catch (e) {
        errEl.textContent = "Could not reach server.";
    }
}

async function verifyCode() {
    const username = document.getElementById("loginUsername").value.trim();
    const code     = document.getElementById("loginCode").value.trim();
    const errEl    = document.getElementById("loginError");
    const infoEl   = document.getElementById("loginInfo");
    errEl.textContent  = "";
    infoEl.textContent = "";

    if (!username || !code) { errEl.textContent = "Enter username and code."; return; }

    try {
        const res  = await fetch(`${API}/api/verify-code`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, code })
        });
        const data = await res.json();
        if (data.error) { errEl.textContent = data.error; return; }

        saveSession(data.token, data.username);
        enterGame(data.balance);
    } catch (e) {
        errEl.textContent = "Could not reach server.";
    }
}

function enterGame(balance) {
    document.getElementById("navUsername").textContent = currentUser;
    document.getElementById("balance").textContent = "Balance: " + balance.toLocaleString();
    document.getElementById("result").textContent  = "Roll result: —";
    showPage("pageGame");
}

function logout() {
    clearSession();
    document.getElementById("loginUsername").value = "";
    document.getElementById("loginCode").value     = "";
    document.getElementById("loginCodeSection").style.display = "none";
    clearAuthMessages();
    showPage("pageAuth");
}

let lastRoll = null;

function roll(amount, label, allin = false) {
    setButtons(false);
    lastRoll = { amount, label, allin };
    const body = allin ? { allin: true } : { amount };

    fetch(`${API}/api/roll`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(body)
    })
    .then(res => res.text())
    .then(text => {
        if (!text || text.trim() === "") throw new Error("Server returned an empty response");

        let data;
        try { data = JSON.parse(text); }
        catch (e) { throw new Error("Bad JSON from server: " + text.slice(0, 100)); }

        if (data.error) {
            document.getElementById("result").textContent = "Error: " + data.error;
            document.getElementById("result").style.color = "#e05c5c";
            stopAutoRoll();
            setButtons(true);
            return;
        }

        const net  = data.rolled - data.bet;
        const sign = net >= 0 ? "+" : "";

        const resultEl = document.getElementById("result");
        resultEl.textContent =
            `${label} → rolled ${data.rolled.toLocaleString()} (${sign}${net.toLocaleString()})`;
        resultEl.style.color = net >= 0 ? "#4caf82" : "#e05c5c";

        document.getElementById("balance").textContent =
            "Balance: " + data.balance.toLocaleString();

        const autoOn = document.getElementById("autoroll").checked;
        if (autoOn && lastRoll && !lastRoll.allin) {
            setTimeout(() => {
                if (document.getElementById("autoroll").checked) {
                    roll(lastRoll.amount, lastRoll.label, lastRoll.allin);
                } else {
                    setButtons(true);
                }
            }, 700);
        } else {
            document.getElementById("autoroll").checked = false;
            setTimeout(() => setButtons(true), 700);
        }
    })
    .catch(err => {
        const resultEl = document.getElementById("result");
        resultEl.textContent = "Error: " + err.message;
        resultEl.style.color = "#e05c5c";
        stopAutoRoll();
        setButtons(true);
    });
}

function stopAutoRoll() {
    document.getElementById("autoroll").checked = false;
}

function setButtons(enabled) {
    ["buttonallin","button1k","button5k","button10k","button25k",
     "button100k","button300k","button700k","button1m","buttonDeposit","buttonCustom"]
        .forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.disabled = !enabled;
        });
}

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("buttonallin").onclick  = () => roll(null,      "ALL IN", true);
    document.getElementById("button1k").onclick     = () => roll(1_000,     "1k");
    document.getElementById("button5k").onclick     = () => roll(5_000,     "5k");
    document.getElementById("button10k").onclick    = () => roll(10_000,    "10k");
    document.getElementById("button25k").onclick    = () => roll(25_000,    "25k");
    document.getElementById("button100k").onclick   = () => roll(100_000,   "100k");
    document.getElementById("button300k").onclick   = () => roll(300_000,   "300k");
    document.getElementById("button700k").onclick   = () => roll(700_000,   "700k");
    document.getElementById("button1m").onclick     = () => roll(1_000_000, "1M");

    document.getElementById("buttonCustom").onclick = () => {
        const input  = document.getElementById("customAmount");
        const amount = parseInt(input.value);
        if (!amount || amount <= 0) return;
        input.value = "";
        roll(amount, amount.toLocaleString());
    };

    document.getElementById("buttonDeposit").onclick = () => {
        const input  = document.getElementById("depositAmount");
        const amount = parseInt(input.value);
        if (!amount || amount <= 0) return;

        fetch(`${API}/api/deposit`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ amount })
        })
        .then(r => r.json())
        .then(d => {
            document.getElementById("balance").textContent =
                "Balance: " + d.balance.toLocaleString();
            input.value = "";
        })
        .catch(err => console.error("Deposit error:", err));
    };

    if (sessionToken) {
        fetch(`${API}/api/balance`, { headers: authHeaders() })
            .then(r => r.json())
            .then(d => {
                if (d.error) { clearSession(); showPage("pageAuth"); return; }
                enterGame(d.balance);
            })
            .catch(() => { clearSession(); showPage("pageAuth"); });
    }
});