def calculator():
    print("=== Калькулятор ===")
    print("Доступные операции: +, -, *, /, //, %, **")
    print("Введите 'q' для выхода\n")
    
    while True:
        try:
            # Получаем первое число
            first = input("Первое число (или 'q' для выхода): ").strip()
            if first.lower() == 'q':
                print("До свидания!")
                break
            
            # Получаем знак операции
            operator = input("Операция (+, -, *, /, //, %, **): ").strip()
            if operator not in ('+', '-', '*', '/', '//', '%', '**'):
                print("Ошибка: неизвестная операция\n")
                continue
            
            # Получаем второе число
            second = input("Второе число: ").strip()
            
            # Преобразуем в числа (поддерживаем и целые, и дробные)
            try:
                a = float(first)
                b = float(second)
            except ValueError:
                print("Ошибка: введите корректные числа\n")
                continue
            
            # Выполняем операцию
            if operator == '+':
                result = a + b
            elif operator == '-':
                result = a - b
            elif operator == '*':
                result = a * b
            elif operator == '/':
                if b == 0:
                    print("Ошибка: деление на ноль\n")
                    continue
                result = a / b
            elif operator == '//':
                if b == 0:
                    print("Ошибка: деление на ноль\n")
                    continue
                result = a // b
            elif operator == '%':
                if b == 0:
                    print("Ошибка: деление на ноль\n")
                    continue
                result = a % b
            elif operator == '**':
                result = a ** b
            
            # Красивый вывод результата
            if result == int(result):
                result = int(result)
            print(f"Результат: {a} {operator} {b} = {result}\n")
        
        except KeyboardInterrupt:
            print("\nПрервано пользователем")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")


if __name__ == "__main__":
    calculator()


