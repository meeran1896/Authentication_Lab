from flask import Flask, request, render_template_string,send_from_directory, abort
import random,os
import time

app = Flask(__name__)

# ⚠️ REAL FLAG (not shown to students)
REAL_FLAG = "CTF{vulnerable_xor_rng}"

FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secure_files_SC')

# Time window (students know this)
START_TIME = int(time.mktime(time.strptime("2026-01-24 19:00:00", "%Y-%m-%d %H:%M:%S")))
END_TIME   = int(time.mktime(time.strptime("2026-01-24 21:00:00", "%Y-%m-%d %H:%M:%S")))

# Pick seed ONCE when server starts
SEED = random.randint(START_TIME, END_TIME)
random.seed(SEED)

# Generate ciphertext once
CIPHERTEXT = [random.randint(0, 255) ^ ord(c) for c in REAL_FLAG]

HTML = """
<h2>🔐 RNG XOR Challenge</h2>

<p><b>Ciphertext:</b></p>
<pre>{{ ciphertext }}</pre>

<p>FLAG format: <b>CTF{XXXXXXX}</b></p>

<form method="POST">
    Guess the seed:<br>
    <input name="seed">
    <input type="submit">
</form>

<p style="color:red;">{{ error }}</p>
<p style="color:green;">{{ success }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def challenge():
    error = ""
    success = ""

    if request.method == "POST":
        try:
            guess = int(request.form["seed"])
            if guess == SEED:
                # Decrypt flag
                random.seed(SEED)
                decrypted = "".join(
                    chr(random.randint(0, 255) ^ c) for c in CIPHERTEXT
                )
                success = "✅ Correct! FLAG = {}".format(decrypted)
            else:
                error = "❌ Wrong seed!"
        except:
            error = "Invalid input"

    return render_template_string(
        HTML,
        ciphertext=CIPHERTEXT,
        error=error,
        success=success
    )

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
