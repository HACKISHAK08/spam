from flask import Flask, request, jsonify
import requests, json, time

app = Flask(__name__)
KEY2 = "projects_xxx_3ei93k_codex_xdfox"
ACCS_FILE = "accs.txt"

def get_jwt(uid, password):
    try:
        url = f"https://projects-fox-x-get-jwt.vercel.app/get?uid={uid}&password={password}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if data.get("status") == "success":
            return data["token"]
    except:
        return None

def send_friend_request(token, target_uid):
    try:
        url = f"https://projects-fox-apis.vercel.app/adding_friend?token={token}&id={target_uid}&key={KEY2}"
        res = requests.get(url, timeout=10)
        return "success" in res.text
    except:
        return False

@app.route("/spam_ishak", methods=["GET"])
def spam_ishak():
    target_uid = request.args.get("uid")
    if not target_uid:
        return jsonify({"error": "uid is required"}), 400

    try:
        with open(ACCS_FILE, "r") as f:
            accounts = json.load(f)
    except:
        return jsonify({"error": "accs.txt missing or invalid format"}), 500

    log = []
    for uid, password in accounts.items():
        jwt = get_jwt(uid, password)
        if not jwt:
            log.append({"uid": uid, "status": "❌ JWT failed"})
            continue

        success = send_friend_request(jwt, target_uid)
        status = "✅ sent" if success else "⚠️ failed"
        log.append({"uid": uid, "status": status})
        time.sleep(1)

    return jsonify({
        "target_uid": target_uid,
        "results": log,
        "total": len(log)
    })

if __name__ == "__main__":
    app.run(port=5000)