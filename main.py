from flask import *
from profiler import profiler

# flaskの初期化
app = Flask(__name__)

# 自作プロファイラの読み込み
profiler(app)

# SSTI endpoint
@app.route("/ssti", methods=["POST"])
def ssti_get():
    return render_template_string(request.form["name"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

a = config.items()
