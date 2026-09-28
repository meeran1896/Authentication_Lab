from flask import Flask, request, render_template_string, session, send_from_directory, abort
import random
import binascii, os

app = Flask(__name__)
app.secret_key = "superweaksecret"

USERS = {
    "admin@meeran.com": "admin"
}

# ❌ Secret hidden from students (but brute-forceable)
SECRET_CONSTANT = "1337"  # assume attacker only knows range 1996–2026

FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secure_files_SC')

LOGIN_HTML = """
<h2>Login</h2>
<form method="POST">
  Email: <input name="email"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit">
</form>
<p style="color:red;">{{ error }}</p>
"""

OTP_HTML = """
<h2>Enter OTP</h2>
<form method="POST" action="/otp">
  OTP: <input name="otp"><br>
  <input type="submit">
</form>
<p style="color:red;">{{ error }}</p>
"""

SUCCESS_HTML = """
<h2>Welcome {{ user }}</h2>
<p>Login successful!</p>
<p>FLAG = CTF{predictable_otp_seed}</p>
"""

# ❌ Weak OTP generator (predictable seed)
def generate_otp(email):
    email_hex = binascii.hexlify(email.encode()).decode()
    seed_string = str(len(email)) + email_hex + SECRET_CONSTANT
    
    random.seed(seed_string)
    return str(random.randint(1000, 9999))

@app.route("/", methods=["GET", "POST"])
def login():
    error = "Invalid credentials"

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")

        if email in USERS and USERS[email] == pwd:
            session["email"] = email
            
            otp = generate_otp(email)
            print("[DEBUG] OTP:", otp)  # ❌ info leak
            
            return render_template_string(OTP_HTML)

        error = "Invalid credentials"

    return render_template_string(LOGIN_HTML, error=error)


@app.route("/otp", methods=["POST"])
def otp():
    email = session.get("email")

    if not email:
        return "Session expired — login again", 403

    user_otp = request.form.get("otp")
    real_otp = generate_otp(email)

    if user_otp == real_otp:
        return render_template_string(SUCCESS_HTML, user=email)

    return render_template_string(OTP_HTML, error="Invalid OTP")

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
