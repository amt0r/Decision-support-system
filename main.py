import sys
from PyQt6.QtWidgets import QApplication
from core.database import Database
from core.engine import InferenceEngine
from ui.gui import MainWindow

def main():
    db = Database()
    db.initialize()
    db.populate_initial_data()
    
    engine = InferenceEngine(db)
    
    app = QApplication(sys.argv)
    window = MainWindow(db, engine)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
