from flask import Flask, render_template_string

app = Flask(__name__)

LOGIN_PAGE = """
<h2>Login</h2>
<form onsubmit="fakeLogin(event)">
  Username: <input id="user"><br>
  Password: <input id="pass" type="password"><br>
  <button type="submit">Login</button>
</form>

<script>
function fakeLogin(e) {
  e.preventDefault();

  let u = document.getElementById("user").value;
  let p = document.getElementById("pass").value;
  if (u === "admin" && p === "password") {
    window.location = "/dashboard";
  } else {
    alert("Login failed");
  }
}
</script>
"""

@app.route("/")
def login():
    return render_template_string(LOGIN_PAGE)

@app.route("/dashboard")
def dashboard():
    return "<h2>Welcome Admin</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 80, debug=True)
