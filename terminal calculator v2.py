import tkinter as tk
import ast
import operator
import math

# Безопасный вычислитель выражений
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expr):
    """Безопасно вычисляет математическое выражение из строки."""
    expr = expr.replace('^', '**').replace('×', '*').replace('÷', '/')
    node = ast.parse(expr, mode='eval').body

    def _eval(n):
        if isinstance(n, ast.Constant):  # Python 3.8+
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Недопустимый тип данных")
        elif isinstance(n, ast.BinOp):
            op = OPERATORS.get(type(n.op))
            if op is None:
                raise ValueError("Неподдерживаемая операция")
            return op(_eval(n.left), _eval(n.right))
        elif isinstance(n, ast.UnaryOp):
            op = OPERATORS.get(type(n.op))
            if op is None:
                raise ValueError("Неподдерживаемый унарный оператор")
            return op(_eval(n.operand))
        else:
            raise ValueError("Недопустимое выражение")

    return _eval(node)


class TerminalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CALC_TERM // v2.0")
        self.root.geometry("420x620")
        self.root.resizable(False, False)

        # Цветовая палитра терминала
        self.bg_color = "#0D1117"       # Глубокий темный фон
        self.panel_color = "#161B22"    # Фон кнопок
        self.fg_color = "#00FF41"       # Матричный зеленый
        self.dim_color = "#008F11"      # Приглушенный зеленый для истории
        self.accent_color = "#1F2937"   # Цвет при наведении
        self.error_color = "#FF3333"    # Цвет ошибки

        self.root.configure(bg=self.bg_color)
        self.font_mono = ("Consolas", 13)
        self.font_input = ("Consolas", 18, "bold")
        self.font_btn = ("Consolas", 14, "bold")

        self.setup_ui()
        self.bind_keys()
        self.log_message("SYSTEM READY. TYPE EXPRESSION OR USE KEYPAD.")

    def setup_ui(self):
        # 1. Окно истории (Лог терминала)
        self.log_box = tk.Text(
            self.root,
            height=10,
            bg=self.bg_color,
            fg=self.dim_color,
            font=self.font_mono,
            bd=1,
            relief="solid",
            highlightbackground=self.dim_color,
            highlightthickness=1,
            state="disabled",
            padx=10,
            pady=10
        )
        self.log_box.pack(fill="x", padx=15, pady=(15, 10))
        self.log_box.tag_config("error", foreground=self.error_color)
        self.log_box.tag_config("result", foreground=self.fg_color)

        # 2. Командная строка ввода
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill="x", padx=15, pady=(0, 15))

        prompt_lbl = tk.Label(
            input_frame,
            text="calc@v2:~$",
            bg=self.bg_color,
            fg=self.fg_color,
            font=self.font_mono
        )
        prompt_lbl.pack(side="left", padx=(0, 8))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            input_frame,
            textvariable=self.entry_var,
            bg=self.panel_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=self.font_input,
            bd=1,
            relief="solid",
            highlightbackground=self.fg_color,
            highlightthickness=1
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.focus_set()

        # 3. Сетка кнопок
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        buttons = [
            ["CLS", "(", ")", "DEL"],
            ["7",   "8", "9", "/"],
            ["4",   "5", "6", "*"],
            ["1",   "2", "3", "-"],
            ["0",   ".", "^", "+"],
            ["SQRT", "EXEC (=)"]
        ]

        for r, row in enumerate(buttons):
            btn_frame.rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                btn_frame.columnconfigure(c, weight=1)
                
                # Кнопка "=" занимает 3 колонки в последнем ряду
                colspan = 3 if label == "EXEC (=)" else 1
                
                btn = tk.Button(
                    btn_frame,
                    text=label,
                    bg=self.panel_color,
                    fg=self.fg_color,
                    activebackground=self.fg_color,
                    activeforeground=self.bg_color,
                    font=self.font_btn,
                    bd=1,
                    relief="solid",
                    cursor="hand2",
                    command=lambda val=label: self.on_button_click(val)
                )
                btn.grid(
                    row=r,
                    column=c,
                    columnspan=colspan,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear_input())

    def log_message(self, text, tag=None):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {text}\n", tag)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def clear_input(self):
        self.entry_var.set("")

    def clear_all(self):
        self.clear_input()
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.log_message("BUFFER CLEARED.")

    def on_button_click(self, val):
        current = self.entry_var.get()

        if val == "CLS":
            self.clear_all()
        elif val == "DEL":
            self.entry_var.set(current[:-1])
        elif val == "EXEC (=)":
            self.calculate()
        elif val == "SQRT":
            self.calculate_sqrt()
        else:
            self.entry_var.set(current + val)

    def calculate_sqrt(self):
        expr = self.entry_var.get().strip()
        if not expr:
            return
        try:
            val = float(safe_eval(expr))
            if val < 0:
                raise ValueError("Корень из отрицательного числа")
            res = round(math.sqrt(val), 8)
            if res.is_integer():
                res = int(res)
            self.log_message(f"sqrt({expr}) = {res}", "result")
            self.entry_var.set(str(res))
        except Exception as e:
            self.log_message(f"ERR: {e}", "error")

    def calculate(self):
        expr = self.entry_var.get().strip()
        if not expr:
            return

        # Поддержка текстовых команд терминала
        if expr.lower() in ("clear", "cls"):
            self.clear_all()
            return
        if expr.lower() == "exit":
            self.root.destroy()
            return

        try:
            result = safe_eval(expr)
            if isinstance(result, float):
                result = round(result, 8)
                if result.is_integer():
                    result = int(result)
            
            self.log_message(f"{expr} = {result}", "result")
            self.entry_var.set(str(result))
        except ZeroDivisionError:
            self.log_message("ERR: DIVISION BY ZERO", "error")
        except Exception:
            self.log_message(f"ERR: SYNTAX ERROR IN '{expr}'", "error")


if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalCalculator(root)
    root.mainloop()

