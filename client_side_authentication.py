from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

USERS = {
    "user": "user123",
    "admin": "securepassword"
}

LOGIN_HTML = """
<h2>Login</h2>
<form method="POST">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <input type="submit">
</form>
<p style="color:red;">{{ error }}</p>
"""

HOME_HTML = """
<h2>Welcome {{ user }}</h2>
<p>You are logged in.</p>
<p><a href="/admin">Go to Admin Page</a></p>
"""

ADMIN_DASHBOARD = """
<h2>🔥 ADMIN PANEL 🔥</h2>
<p>FLAG = CTF{client_side_cookie_auth}</p>
"""

NO_ACCESS_HTML = """
<h2>Access Denied</h2>
<p>❌ Only admin can see this page</p>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    error = "Invalid credentials"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            resp = make_response(render_template_string(HOME_HTML, user=username))

            # ❌ Vulnerable: Role stored in client cookie
            if username == "admin":
                resp.set_cookie("role", "admin")
            else:
                resp.set_cookie("role", "user")

            resp.set_cookie("username", username)

            return resp

        error = "Login failed"

    return render_template_string(LOGIN_HTML, error=error)


@app.route("/admin")
def admin():
    role = request.cookies.get("role")
    username = request.cookies.get("username")

    if not role or not username:
        return "Not logged in", 403

    # ❌ Vulnerable: Trusting client-side cookie for authorization
    if role == "admin":
        return render_template_string(ADMIN_DASHBOARD)

    return render_template_string(NO_ACCESS_HTML)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
