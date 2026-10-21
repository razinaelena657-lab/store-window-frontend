# app.py — требуется: pip install flask
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            op = request.form["op"]

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                if b == 0:
                    error = "Деление на ноль"
                else:
                    result = a / b
            else:
                error = "Неизвестная операция"

        except (ValueError, KeyError):
            error = "Некорректный ввод"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)


