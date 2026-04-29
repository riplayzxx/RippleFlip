import random
import string
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/front.js")
def js():
    return send_from_directory(".", "front.js")


# ── In-memory stores ──────────────────────────────────────────────
accounts = {}          # { mc_username: { "balance": int } }
pending_codes = {}     # { mc_username: "123456" }
sessions = {}          # { session_token: mc_username }


def gen_token(n=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


# ── Auth endpoints ────────────────────────────────────────────────

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400
    if username in accounts:
        return jsonify({"error": "Username already registered"}), 400
    accounts[username] = {"balance": 0}
    return jsonify({"ok": True})


@app.route("/api/request-code", methods=["POST"])
def request_code():
    """Generate a 6-digit code for the given MC username."""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400
    if username not in accounts:
        return jsonify({"error": "Username not found — sign up first"}), 404
    code = str(random.randint(100000, 999999))
    pending_codes[username] = code
    print(f"[DEV] Code for {username}: {code}")
    return jsonify({"ok": True, "dev_code": code})


@app.route("/api/verify-code", methods=["POST"])
def verify_code():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    code = (data.get("code") or "").strip()
    if not username or not code:
        return jsonify({"error": "Username and code required"}), 400
    if username not in accounts:
        return jsonify({"error": "Username not found"}), 404
    if pending_codes.get(username) != code:
        return jsonify({"error": "Incorrect code"}), 401
    del pending_codes[username]
    token = gen_token()
    sessions[token] = username
    return jsonify({"ok": True, "token": token, "username": username,
                    "balance": accounts[username]["balance"]})


# ── Helper ────────────────────────────────────────────────────────

def get_user(req):
    """Return (username, error_response) from Authorization header."""
    auth = req.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "").strip()
    username = sessions.get(token)
    if not username:
        return None, (jsonify({"error": "Not logged in"}), 401)
    return username, None


@app.route("/api/roll", methods=["POST"])
def api_roll():
    username, err = get_user(request)
    if err:
        return err
    try:
        data = request.get_json(silent=True) or {}
        allin = data.get("allin", False)
        balance = accounts[username]["balance"]

        if allin:
            amount = balance
        else:
            try:
                amount = int(data.get("amount", 0))
            except (TypeError, ValueError):
                amount = 0

        if amount <= 0:
            return jsonify({"error": "Nothing to bet — balance is 0"}), 400
        if amount > balance:
            return jsonify({"error": "Not enough balance"}), 400

        accounts[username]["balance"] -= amount

        a = int(amount)
        b = a * 2
        branch = random.randint(1, 5) if amount <= 15_000_000 else random.randint(1, 4)
        result = random.randint(1, a) if branch <= 4 else random.randint(a, b)

        accounts[username]["balance"] += result
        return jsonify({"rolled": result, "bet": amount,
                        "balance": accounts[username]["balance"]})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/balance")
def balance():
    username, err = get_user(request)
    if err:
        return err
    return jsonify({"balance": accounts[username]["balance"]})


@app.route("/api/deposit", methods=["POST"])
def deposit():
    username, err = get_user(request)
    if err:
        return err
    data = request.get_json(silent=True) or {}
    try:
        amount = int(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    accounts[username]["balance"] += amount
    return jsonify({"balance": accounts[username]["balance"]})


if __name__ == "__main__":
    app.run(debug=True)