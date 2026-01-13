from flask import Flask, request, escape, jsonify
import hashlib
import subprocess
import os

app = Flask(__name__)

# ✅ Sécurisation du mot de passe
# Ne jamais stocker en dur : utiliser les variables d'environnement
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    raise ValueError("ADMIN_PASSWORD doit être défini comme variable d'environnement")

# ✅ Hachage sécurisé (SHA-256 au lieu de MD5)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    if username == "admin" and hash_password(password) == hash_password(ADMIN_PASSWORD):
        return jsonify({"message": "Logged in"}), 200

    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "localhost")

    # ✅ Exécution sécurisée sans shell=True
    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", host],
            stderr=subprocess.STDOUT,
            timeout=3
        )
        return jsonify({"ping_result": result.decode("utf-8")})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Ping failed"}), 400
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timed out"}), 408

@app.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "user")
    
    # ✅ Protection contre XSS
    safe_name = escape(name)
    return f"<h1>Hello {safe_name}</h1>"

if __name__ == "__main__":
    # ✅ Debug désactivé pour production
    app.run(host="0.0.0.0", port=5000, debug=False)
