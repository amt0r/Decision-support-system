from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from database import Database
from engine import InferenceEngine
from gui_styles import MAIN_STYLE
from gui_welcome import WelcomePage
from gui_questionnaire import QuestionnairePage
from gui_results import ResultsPage
from gui_admin import AdminPanelPage, AdminLoginDialog

class MainWindow(QMainWindow):
    def __init__(self, db: Database, engine: InferenceEngine):
        super().__init__()
        self._db = db
        self._engine = engine
        self.setWindowTitle("DSS: Підбір резервного живлення")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet(MAIN_STYLE)
        
        self._stacked = QStackedWidget()
        self.setCentralWidget(self._stacked)
        
        self._welcome = WelcomePage(self._start_questionnaire, self._open_admin)
        self._questionnaire = QuestionnairePage(self._db, self._show_results, self._show_welcome)
        self._results = ResultsPage(self._start_questionnaire, self._show_welcome)
        self._admin = AdminPanelPage(self._db, self._show_welcome)
        
        self._stacked.addWidget(self._welcome)
        self._stacked.addWidget(self._questionnaire)
        self._stacked.addWidget(self._results)
        self._stacked.addWidget(self._admin)
        
        self._show_welcome()

    def _show_welcome(self):
        self._stacked.setCurrentWidget(self._welcome)

    def _start_questionnaire(self):
        questions = self._db.get_all_questions()
        options = self._db.get_all_options()
        if not questions:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Неможливо розпочати",
                "У базі даних немає жодного запитання.\n"
                "Додайте принаймні одне запитання через панель адміністратора.")
            return
        if not options:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Неможливо розпочати",
                "У базі даних немає жодного рішення (обладнання).\n"
                "Додайте принаймні одне рішення через панель адміністратора.")
            return
        self._questionnaire.start()
        self._stacked.setCurrentWidget(self._questionnaire)

    def _show_results(self, answers):
        recommendations = self._engine.get_top_recommendations(answers, top_n=10)
        if not recommendations:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Немає результатів",
                "Система не змогла підібрати жодного рішення.\n"
                "Можливо, у базі немає обладнання або правил.")
            self._show_welcome()
            return
        self._results.show_results(recommendations)
        self._stacked.setCurrentWidget(self._results)

    def _open_admin(self):
        dialog = AdminLoginDialog(self._db, self)
        if dialog.exec() and dialog.is_authenticated:
            self._admin.load_data()
            self._stacked.setCurrentWidget(self._admin)
