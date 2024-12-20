import sys

from PyQt6.QtWidgets import QApplication

from gui import CalculatorGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CalculatorGUI()
    gui.run()
    sys.exit(app.exec())