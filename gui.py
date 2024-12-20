import sys

from PyQt6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton,
                             QTabWidget, QVBoxLayout, QWidget)

from calc_functions import Calculator
from graphics import plot_linear, plot_quadratic, plot_trig


class StandardCalculator(QWidget):
    """Калькулятор с интерфейсом, соответствующим дизайну"""
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()  
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Поле ввода
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("font-size: 24px; color: white; background-color: black;")
        main_layout.addWidget(self.display)

        # Панель управления памятью
        memory_layout = QHBoxLayout()

        # Кнопки памяти
        memory_buttons = ['mc', 'mr', 'm+', 'm-', 'ms', 'm:']
        for text in memory_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_function_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            memory_layout.addWidget(btn)

        # Добавляем панель памяти под строку ввода
        main_layout.addLayout(memory_layout)

        # Основной контейнер для числовых кнопок и групп справа
        central_layout = QHBoxLayout()

        # Сетка для кнопок
        buttons_layout = QGridLayout()

        # Числовые кнопки
        num_buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 1), ('.', 3, 2)
        ]
        for text, row, col in num_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_number_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            buttons_layout.addWidget(btn, row, col)

        btn_change = QPushButton("+/-")
        btn_change.clicked.connect(self.on_function_click)
        btn_change.setStyleSheet("font-size: 16px;")
        buttons_layout.addWidget(btn_change, 3, 0)
        # Кнопка "C" и "="
        btn_C = QPushButton("C")
        btn_C.clicked.connect(self.on_function_click)
        btn_C.setStyleSheet("font-size: 16px;")
        buttons_layout.addWidget(btn_C, 4, 0)

        btn_equal = QPushButton("=")
        btn_equal.clicked.connect(self.on_function_click)
        btn_equal.setStyleSheet("font-size: 16px;")
        buttons_layout.addWidget(btn_equal, 4, 2)

        # Добавляем сетку числовых кнопок в центральный макет
        central_layout.addLayout(buttons_layout)

        # Боковая панель с QGroupBox
        side_layout = QVBoxLayout()

        # Операции
        operations_group = QGroupBox()
        operations_layout = QVBoxLayout()
        operations_buttons = ['+', '-', '*', '/']
        for text in operations_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_function_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            operations_layout.addWidget(btn)
        operations_group.setLayout(operations_layout)
        operations_group.setStyleSheet("border: 2px solid yellow;")

        # Тригонометрия
        trig_group = QGroupBox()
        trig_layout = QVBoxLayout()
        trig_buttons = ['sin', 'cos']
        for text in trig_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_function_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            trig_layout.addWidget(btn)
        trig_group.setLayout(trig_layout)
        trig_group.setStyleSheet("border: 2px solid orange;")

        # Специальные функции
        special_group = QGroupBox()
        special_layout = QVBoxLayout()
        special_buttons = ['sqrt', '^', 'mod']
        for text in special_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_function_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            special_layout.addWidget(btn)
        special_group.setLayout(special_layout)
        special_group.setStyleSheet("border: 2px solid pink;")

        # Остальные функции
        other_group = QGroupBox()
        other_layout = QVBoxLayout()
        other_buttons = ['floor', 'ceil']
        for text in other_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, btn=text: self.on_function_click(btn))
            btn.setStyleSheet("font-size: 16px;")
            other_layout.addWidget(btn)
        other_group.setLayout(other_layout)
        other_group.setStyleSheet("border: 2px solid brown;")

        # Добавляем все группы на боковую панель
        side_layout.addWidget(operations_group)
        side_layout.addWidget(trig_group)
        side_layout.addWidget(special_group)
        side_layout.addWidget(other_group)

        # Добавляем боковую панель в центральный макет
        central_layout.addLayout(side_layout)

        # Добавляем центральный макет в основной макет
        main_layout.addLayout(central_layout)

        self.setLayout(main_layout)

    def on_number_click(self, btn):
        current_text = self.display.text()
        if current_text == "0":
            self.display.setText(btn)
        else:
            self.display.setText(current_text + btn)

    def on_function_click(self, btn=None):
        text = btn if btn else self.sender().text()
        current_text = self.display.text()
        
        try:
            if text == "C":
                # Очистка поля ввода
                self.calculator.clear()
                self.display.setText("0")
            
            elif text == "+/-":
            # Change the sign of the first non-zero number
                if current_text == "0":
                    self.display.setText("-0")
                    self.calculator.current_value = -0
                elif " " in current_text:
                    QMessageBox.warning(self, "Ошибка", "Невозможно изменить знак у сложного выражения")
                else:
                    try:
                        value = float(current_text)
                        self.calculator.current_value = value
                        result = self.calculator.change_sign()
                        self.display.setText(str(result))
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Некорректное число в поле ввода")
            
            elif text in "+-*/^mod":
            # Добавление оператора в строку ввода
                if " " in current_text:
                    QMessageBox.warning(self, "Error", "Only one operation is allowed at a time")
                else:
                    self.display.setText(current_text + f" {text} ")
            
            elif text in ["sin", "cos", "sqrt", "floor", "ceil"]:
                # Вычисление функции
                value = float(current_text)
                self.calculator.current_value = value

                if text == "sin":
                    result = self.calculator.sin()
                elif text == "cos":
                    result = self.calculator.cos()
                elif text == "sqrt":
                    result = self.calculator.sqrt()
                elif text == "floor":
                    result = self.calculator.floor()
                elif text == "ceil":
                    result = self.calculator.ceil()
                
                self.display.setText(str(result))
            
            elif text == "=":
                # Вычисление результата
                if " " in current_text:
                    parts = current_text.split()
                    if len(parts) == 3:
                        left, op, right = parts
                        left, right = float(left), float(right)
                        self.calculator.current_value = left
                        
                        if op == "+":
                            result = self.calculator.add(right)
                        elif op == "-":
                            result = self.calculator.subtract(right)
                        elif op == "*":
                            result = self.calculator.multiply(right)
                        elif op == "/":
                            result = self.calculator.divide(right)
                        elif op == "mod":
                            result = self.calculator.remainder(right)
                        elif op == "^":
                            result = self.calculator.pow(right)
                        self.display.setText(str(result))
            
            elif text == "m:":
                # Отображение памяти
                memory_value = self.calculator.memory
                QMessageBox.information(self, "Memory", f"Memory: {memory_value}")
            elif text == "mc":  # Очистка памяти
                self.calculator.memory_clear()
                QMessageBox.information(self, "Memory", "Memory cleared")

            elif text == "mr":  # Чтение памяти
                self.calculator.memory_recall()
                self.display.setText(str(self.calculator.current_value))

            elif text == "m+":  # Добавление к памяти
                try:
                    value = float(self.display.text())
                    self.calculator.memory_add(value)
                    QMessageBox.information(self, "Memory", f"Added to memory: {value}")
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректное значение для добавления в память")

            elif text == "m-":  # Вычитание из памяти
                try:
                    value = float(self.display.text())
                    self.calculator.memory_subtract(value)
                    QMessageBox.information(self, "Memory", f"Subtracted from memory: {value}")
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректное значение для вычитания из памяти")

            elif text == "ms":  # Сохранение в память
                try:
                    value = float(self.display.text())
                    self.calculator.memory = value
                    QMessageBox.information(self, "Memory", f"Saved to memory: {value}")
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректное значение для сохранения в память")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", "Invalid operation")
            
            
class GraphicsCalculator(QWidget):
    """Вкладка для построения графиков"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для ввода уравнений
        self.equation_input = QLineEdit()
        self.equation_input.setPlaceholderText("Введите уравнение, например 2x + 3 = y")
        layout.addWidget(self.equation_input)

        # Кнопка построения
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot_graph(self):
        equation = self.equation_input.text()
        try:
            if "=" not in equation:
                raise ValueError("Уравнение должно содержать знак '='")
            lhs, rhs = equation.split('=')
            rhs = rhs.strip()
            lhs = lhs.strip()

            # Проверяем тип уравнения
            if "x**2" in lhs or "x^2" in lhs:
                a, b, c = self.parse_quadratic(lhs)
                plot_quadratic(a, b, c)
            elif "sin" in lhs or "cos" in lhs or "tan" in lhs:
                func_type = self.parse_trig(lhs)
                plot_trig(func_type)
            else:
                a, b = self.parse_linear(lhs)
                plot_linear(a, b)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка построения: {e}")

    def parse_linear(self, expression):
        """Парсинг линейного уравнения вида ax + b"""
        expression = expression.replace("x", "").strip()
        parts = expression.split("+")
        a = float(parts[0]) if parts[0] else 1
        b = float(parts[1]) if len(parts) > 1 else 0
        return a, b

    def parse_quadratic(self, expression):
        """Парсинг квадратного уравнения вида ax^2 + bx + c"""
        expression = expression.replace("x**2", "").replace("x^2", "").replace("x", "")
        parts = expression.split("+")
        a = float(parts[0]) if parts[0] else 1
        b = float(parts[1]) if len(parts) > 1 else 0
        c = float(parts[2]) if len(parts) > 2 else 0
        return a, b, c

    def parse_trig(self, expression):
        """Парсинг тригонометрической функции"""
        if "sin" in expression:
            return "sin"
        elif "cos" in expression:
            return "cos"
        elif "tan" in expression:
            return "tan"
        raise ValueError("Неподдерживаемая тригонометрическая функция")


class CalculatorGUI(QWidget):
    """Основной интерфейс с вкладками"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(200, 200, 500, 500)

        layout = QVBoxLayout()

        # Вкладки
        tabs = QTabWidget()
        tabs.addTab(StandardCalculator(), "Калькулятор")
        tabs.addTab(GraphicsCalculator(), "Графики")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def run(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    gui = CalculatorGUI()
    gui.run()
    sys.exit(app.exec())
