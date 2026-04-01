import sys
from PyQt6.QtWidgets import QApplication
from gui import FitnessApp

def main():
    app = QApplication(sys.argv)
    
    # Optional: Set global font or style here if needed
    
    window = FitnessApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

