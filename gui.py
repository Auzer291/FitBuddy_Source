import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QGroupBox, QStackedWidget,
    QLineEdit, QFormLayout, QTextEdit, QListWidget, QMessageBox,
    QSpinBox, QFrame, QProgressBar, QListWidgetItem, QSizePolicy,
    QGraphicsDropShadowEffect, QFileDialog)
from PyQt6.QtCore import (QTimer, Qt, pyqtSignal, QPropertyAnimation,
                          QEasingCurve, QSize, QPoint, QParallelAnimationGroup, QThread)
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QIcon

from camera import Camera
from pose_estimation import PoseEstimator
from exercise_rules import ExerciseRules
from posture_check import PostureEvaluator
from rep_counter import RepCounter
from feedback import FeedbackSystem
from scoring import Scorer
from angle_calculation import calculate_angle
from planner import WorkoutPlanner
from session_manager import SessionManager
from localization import LocalizationManager
from custom_exercise import CustomExerciseManager, VideoAnalyzer

# ── Theme System ──────────────────────────────
THEMES = {
    "dark": {
        "BG_DEEP": "#0d0d14",
        "BG_SURFACE": "#16162a",
        "BG_CARD": "#1e1e35",
        "BG_CARD2": "#252545",
        "BORDER": "#2a2a4a",
        "BORDER_HL": "#4a4a7a",
        "PRI": "#7c6aff",
        "PRI_LIGHT": "#9d8fff",
        "PRI_DARK": "#5a4adf",
        "SEC": "#00d4b4",
        "SEC_DARK": "#00a88e",
        "DANGER": "#ff4d6d",
        "DANGER_DARK": "#cc3050",
        "TEXT_PRI": "#f0f0ff",
        "TEXT_SEC": "#b0b0d0",
        "TEXT_MUTED": "#6a6a9a",
    },
    "light": {
        "BG_DEEP": "#f4f5f8",
        "BG_SURFACE": "#ffffff",
        "BG_CARD": "#ffffff",
        "BG_CARD2": "#eef0f4",
        "BORDER": "#e2e6ea",
        "BORDER_HL": "#bdc5ce",
        "PRI": "#6b59ff",
        "PRI_LIGHT": "#9284ff",
        "PRI_DARK": "#4b3ad4",
        "SEC": "#00b89d",
        "SEC_DARK": "#008f7a",
        "DANGER": "#fa3c5d",
        "DANGER_DARK": "#cc2844",
        "TEXT_PRI": "#1c1c28",
        "TEXT_SEC": "#5b637a",
        "TEXT_MUTED": "#8e98aa",
    }
}

class Theme:
    current = "dark"
    t = THEMES[current]

def set_theme(name):
    if name in THEMES:
        Theme.current = name
        Theme.t = THEMES[name]

def get_stylesheet():
    t = Theme.t
    return f"""
QWidget {{
    background-color: {t['BG_DEEP']};
    color: {t['TEXT_PRI']};
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
}}
QLabel {{ color: {t['TEXT_PRI']}; background: transparent; }}
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {t['PRI']},stop:1 {t['PRI_DARK']});
    color:#fff; border:none; border-radius:10px;
    padding:12px 24px; font-weight:700; font-size:16px;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {t['PRI_LIGHT']},stop:1 {t['PRI']});
}}
QPushButton:pressed {{ background:{t['PRI_DARK']}; }}
QPushButton:disabled {{ background:{t['BORDER']}; color:{t['TEXT_MUTED']}; }}
QLineEdit, QTextEdit, QSpinBox {{
    background-color:{t['BG_CARD']}; color:{t['TEXT_PRI']};
    border:1px solid {t['BORDER']}; border-radius:8px; padding:8px 12px;
    selection-background-color:{t['PRI']};
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{ border:1px solid {t['PRI']}; }}
QSpinBox::up-button, QSpinBox::down-button {{
    width:20px; background:{t['BG_CARD2']}; border:none; border-radius:4px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background:{t['PRI']}; }}
QComboBox {{
    background-color:{t['BG_CARD']}; color:{t['TEXT_PRI']};
    border:1px solid {t['BORDER']}; border-radius:8px; padding:8px 12px;
}}
QComboBox:focus {{ border:1px solid {t['PRI']}; }}
QComboBox::drop-down {{
    width:30px; border-left:1px solid {t['BORDER']};
    border-top-right-radius:8px; border-bottom-right-radius:8px;
    background:{t['BG_CARD2']};
}}
QComboBox QAbstractItemView {{
    background-color:{t['BG_CARD']}; color:{t['TEXT_PRI']};
    selection-background-color:{t['PRI']}; border:1px solid {t['BORDER']};
}}
QListWidget {{
    background-color:{t['BG_CARD']}; border:1px solid {t['BORDER']};
    border-radius:10px; padding:5px; outline:none;
}}
QListWidget::item {{
    border-radius:8px; padding:10px; margin:2px 0;
}}
QListWidget::item:selected {{ background-color:{t['PRI']}; color:white; }}
QListWidget::item:hover:!selected {{ background-color:{t['BG_CARD2']}; }}
QScrollBar:vertical {{
    background:{t['BG_SURFACE']}; width:8px; border-radius:4px;
}}
QScrollBar::handle:vertical {{
    background:{t['BORDER_HL']}; border-radius:4px; min-height:30px;
}}
QScrollBar::handle:vertical:hover {{ background:{t['PRI']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
QProgressBar {{
    background-color:{t['BG_CARD']}; border:1px solid {t['BORDER']};
    border-radius:8px; text-align:center; color:{t['TEXT_PRI']};
    font-weight:bold; height:20px;
}}
QProgressBar::chunk {{
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {t['PRI']},stop:1 {t['SEC']});
    border-radius:7px;
}}
QGroupBox {{
    border:1px solid {t['BORDER']}; border-radius:12px; margin-top:18px;
    font-weight:bold; color:{t['PRI_LIGHT']}; padding:10px;
}}
QGroupBox::title {{
    subcontrol-origin:margin; left:14px; padding:0 6px;
    background:{t['BG_DEEP']};
}}
"""

# ── Helpers ───────────────────────────────────
def make_shadow(color, blur=20, xoff=0, yoff=3):
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(blur)
    s.setColor(QColor(color))
    s.setOffset(xoff, yoff)
    return s

def make_card(parent=None):
    f = QFrame(parent)
    f.setStyleSheet(f"QFrame{{background:{Theme.t['BG_CARD']};border:1px solid {Theme.t['BORDER']};border-radius:14px;}}")
    return f

def hdivider():
    ln = QFrame()
    ln.setFrameShape(QFrame.Shape.HLine)
    ln.setStyleSheet(f"background:{Theme.t['BORDER']}; border:none;")
    ln.setFixedHeight(1)
    return ln

# ── Button Classes ────────────────────────────
class PrimaryButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_theme()
    def apply_theme(self):
        self.setGraphicsEffect(make_shadow(Theme.t['PRI'], 20, 0, 3))

class SecondaryButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 {Theme.t['SEC']},stop:1 {Theme.t['SEC_DARK']});color:#000;border:none;
                border-radius:10px;padding:12px 24px;font-weight:700;font-size:16px;}}
            QPushButton:hover{{background:{Theme.t['SEC']};}}
            QPushButton:pressed{{background:{Theme.t['SEC_DARK']};}}
        """)
        self.setGraphicsEffect(make_shadow(Theme.t['SEC'], 20, 0, 3))

class AddButton(SecondaryButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setIcon(QIcon("plus_arrow.svg"))
        self.setIconSize(QSize(20, 20))

class OutlineButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton{{background:transparent;color:{Theme.t['TEXT_SEC']};
                border:1px solid {Theme.t['BORDER_HL']};border-radius:10px;
                padding:12px 24px;font-weight:600;font-size:16px;}}
            QPushButton:hover{{border-color:{Theme.t['PRI']};color:{Theme.t['PRI_LIGHT']};
                background:rgba(124,106,255,0.08);}}
            QPushButton:pressed{{background:rgba(124,106,255,0.15);}}
        """)

class DangerButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton{{background:rgba(255,77,109,0.12);color:{Theme.t['DANGER']};
                border:1px solid rgba(255,77,109,0.35);border-radius:10px;
                padding:12px 24px;font-weight:700;font-size:16px;}}
            QPushButton:hover{{background:{Theme.t['DANGER']};color:white;border-color:{Theme.t['DANGER']};}}
            QPushButton:pressed{{background:{Theme.t['DANGER_DARK']};color:white;}}
        """)

class SmallIconButton(QPushButton):
    def __init__(self, text="✕", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(25, 25)
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_MUTED']};
                border:1px solid {Theme.t['BORDER']};border-radius:7px;
                font-size:16px;font-weight:bold;padding:0;}}
            QPushButton:hover{{background:{Theme.t['DANGER']};color:white;border-color:{Theme.t['DANGER']};}}
        """)

class BackButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__()
        if parent: self.setParent(parent)
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(QIcon("back_arrow.svg"))
        self.setIconSize(QSize(24, 24))
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton{{background:transparent;color:{Theme.t['TEXT_PRI']};
                border:1px solid {Theme.t['BORDER_HL']};border-radius:10px;
                padding:8px 16px;font-weight:600;font-size:16px;}}
            QPushButton:hover{{border-color:white;color:white;
                background:rgba(255,255,255,0.08);}}
            QPushButton:pressed{{background:rgba(255,255,255,0.15);}}
        """)

# ── Animated Stacked Widget ───────────────────
class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animating = False

    def slide_to(self, index, direction="left"):
        if self._animating or index == self.currentIndex():
            self.setCurrentIndex(index)
            return
        self._animating = True
        old_w = self.currentWidget()
        self.setCurrentIndex(index)
        new_w = self.currentWidget()
        w = self.width()
        offset = w if direction == "left" else -w
        base = old_w.pos()
        new_w.move(base.x() + offset, base.y())
        new_w.show(); new_w.raise_()
        a1 = QPropertyAnimation(old_w, b"pos"); a1.setDuration(300)
        a1.setStartValue(base); a1.setEndValue(QPoint(base.x() - offset, base.y()))
        a1.setEasingCurve(QEasingCurve.Type.OutCubic)
        a2 = QPropertyAnimation(new_w, b"pos"); a2.setDuration(300)
        a2.setStartValue(QPoint(base.x() + offset, base.y())); a2.setEndValue(base)
        a2.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._grp = QParallelAnimationGroup()
        self._grp.addAnimation(a1); self._grp.addAnimation(a2)
        self._grp.finished.connect(self._done)
        self._grp.start()

    def _done(self): self._animating = False

# ── Screen: Main Menu ─────────────────────────
class MainMenu(QWidget):
    start_workout_signal = pyqtSignal()
    create_session_signal = pyqtSignal()
    custom_ex_signal = pyqtSignal()
    planner_signal = pyqtSignal()
    settings_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, loc_manager):
        super().__init__()
        self.loc = loc_manager
        self._btns = []
        self.init_ui()

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setSpacing(0)

        # Logo area
        logo = QVBoxLayout(); logo.setSpacing(8)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel()
        self.title.setFont(QFont("Segoe UI", 110, QFont.Weight.Black))
        self.title.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};letter-spacing:3px;background:transparent;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.addWidget(self.title)
        self.subtitle = QLabel()
        self.subtitle.setFont(QFont("Segoe UI", 16))
        self.subtitle.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.addWidget(self.subtitle)
        # Accent bar
        self.accentbar = QFrame(); self.accentbar.setFixedSize(120, 3)
        self.accentbar.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {Theme.t['PRI']},stop:1 {Theme.t['SEC']});border-radius:2px;")
        wrap = QHBoxLayout(); wrap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wrap.addWidget(self.accentbar); logo.addLayout(wrap)
        outer.addLayout(logo)
        outer.addSpacing(40)

        # Buttons
        btns_layout = QVBoxLayout(); btns_layout.setSpacing(12)
        btns_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_workout  = PrimaryButton();  self.btn_workout.setFixedWidth(320); self.btn_workout.setMinimumHeight(52)
        self.btn_create   = SecondaryButton(); self.btn_create.setFixedWidth(320);  self.btn_create.setMinimumHeight(52)
        self.btn_custom   = SecondaryButton(); self.btn_custom.setFixedWidth(320);  self.btn_custom.setMinimumHeight(52)
        self.btn_planner  = OutlineButton();  self.btn_planner.setFixedWidth(320); self.btn_planner.setMinimumHeight(52)
        self.btn_settings = OutlineButton();  self.btn_settings.setFixedWidth(320);self.btn_settings.setMinimumHeight(52)
        self.btn_exit     = DangerButton();   self.btn_exit.setFixedWidth(320);    self.btn_exit.setMinimumHeight(52)

        self.btn_workout.clicked.connect(self.start_workout_signal.emit)
        self.btn_create.clicked.connect(self.create_session_signal.emit)
        self.btn_custom.clicked.connect(self.custom_ex_signal.emit)
        self.btn_planner.clicked.connect(self.planner_signal.emit)
        self.btn_settings.clicked.connect(self.settings_signal.emit)
        self.btn_exit.clicked.connect(self.exit_signal.emit)

        self._btns = [self.btn_workout, self.btn_create, self.btn_custom,
                      self.btn_planner, self.btn_settings, self.btn_exit]
        for b in self._btns:
            btns_layout.addWidget(b, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addLayout(btns_layout)
        outer.addSpacing(30)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.title.setText(self.loc.get("app_title"))
        self.subtitle.setText(self.loc.get("subtitle"))
        self.btn_workout.setText("🏋️  " + self.loc.get("btn_start_workout"))
        self.btn_create.setText("💾  "  + self.loc.get("btn_create_session"))
        self.btn_custom.setText("🎥  "  + (self.loc.get("btn_custom_ex") if self.loc.get("btn_custom_ex") != "btn_custom_ex" else "Custom Exercise"))
        self.btn_planner.setText("📋  " + self.loc.get("btn_planner"))
        self.btn_settings.setText("⚙️  " + self.loc.get("btn_settings"))
        self.btn_exit.setText("✕  "    + self.loc.get("btn_exit"))

    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};letter-spacing:3px;background:transparent;")
        self.subtitle.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;")
        self.accentbar.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {Theme.t['PRI']},stop:1 {Theme.t['SEC']});border-radius:2px;")
        for btn in self._btns:
            if hasattr(btn, 'apply_theme'): btn.apply_theme()

    def showEvent(self, e):
        super().showEvent(e)
        for i, b in enumerate(self._btns):
            QTimer.singleShot(i * 90, lambda btn=b: self._fade_in(btn))

    def _fade_in(self, w):
        a = QPropertyAnimation(w, b"windowOpacity")
        a.setDuration(280); a.setStartValue(0.0); a.setEndValue(1.0)
        a.setEasingCurve(QEasingCurve.Type.OutCubic)
        a.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

# ── Screen: Settings ──────────────────────────
class SettingsScreen(QWidget):
    back_signal = pyqtSignal()
    lang_changed_signal = pyqtSignal(str)
    theme_changed_signal = pyqtSignal(str)

    def __init__(self, loc_manager):
        super().__init__()
        self.loc = loc_manager
        self._lang = loc_manager.current_lang
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(24)

        # Header
        hdr = QHBoxLayout()
        self.btn_back = BackButton(); self.btn_back.setFixedWidth(140); self.btn_back.setMinimumHeight(44)
        self.btn_back.clicked.connect(self.back_signal.emit)
        hdr.addWidget(self.btn_back); hdr.addStretch()
        self.title = QLabel()
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self.title); hdr.addStretch(); hdr.addSpacing(140)
        layout.addLayout(hdr)

        # Language card
        self.card = make_card(); cl = QVBoxLayout(self.card)
        cl.setContentsMargins(24, 20, 24, 20); cl.setSpacing(16)
        self.lbl_lang = QLabel()
        self.lbl_lang.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_lang.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        cl.addWidget(self.lbl_lang)
        lr = QHBoxLayout(); lr.setSpacing(12)
        self.btn_en = QPushButton(); self.btn_en.setMinimumHeight(52); self.btn_en.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_vn = QPushButton(); self.btn_vn.setMinimumHeight(52); self.btn_vn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_en.clicked.connect(lambda: self._pick('en'))
        self.btn_vn.clicked.connect(lambda: self._pick('vn'))
        lr.addWidget(self.btn_en); lr.addWidget(self.btn_vn)
        cl.addLayout(lr)
        layout.addWidget(self.card)

        # Theme card
        self.card_theme = make_card(); ct = QVBoxLayout(self.card_theme)
        ct.setContentsMargins(24, 20, 24, 20); ct.setSpacing(16)
        self.lbl_theme = QLabel()
        self.lbl_theme.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_theme.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        ct.addWidget(self.lbl_theme)
        tr = QHBoxLayout(); tr.setSpacing(12)
        self.btn_dark = QPushButton(); self.btn_dark.setMinimumHeight(52); self.btn_dark.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_light = QPushButton(); self.btn_light.setMinimumHeight(52); self.btn_light.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_dark.clicked.connect(lambda: self._pick_theme('dark'))
        self.btn_light.clicked.connect(lambda: self._pick_theme('light'))
        tr.addWidget(self.btn_dark); tr.addWidget(self.btn_light)
        ct.addLayout(tr)
        layout.addWidget(self.card_theme)

        layout.addStretch()
        self.retranslate_ui()

    def _pick_theme(self, theme_name):
        self._refresh_lang_btns(theme_name)
        self.theme_changed_signal.emit(theme_name)

    def _pick(self, lang):
        self._lang = lang
        self._refresh_lang_btns()
        self.lang_changed_signal.emit(lang)

    def _refresh_lang_btns(self, current_theme=None):
        if current_theme is None: current_theme = Theme.current
        active = f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {Theme.t['PRI']},stop:1 {Theme.t['PRI_DARK']});color:white;border:none;border-radius:10px;padding:12px;font-weight:700;font-size:16px;}}"
        inactive = f"QPushButton{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_SEC']};border:1px solid {Theme.t['BORDER']};border-radius:10px;padding:12px;font-size:16px;}} QPushButton:hover{{border-color:{Theme.t['PRI']};color:{Theme.t['PRI_LIGHT']};}}"
        self.btn_en.setStyleSheet(active if self._lang == 'en' else inactive)
        self.btn_vn.setStyleSheet(active if self._lang == 'vn' else inactive)
        self.btn_dark.setStyleSheet(active if current_theme == 'dark' else inactive)
        self.btn_light.setStyleSheet(active if current_theme == 'light' else inactive)

    def retranslate_ui(self):
        self.title.setText(self.loc.get("title_settings"))
        self.btn_back.setText("  " + self.loc.get("back"))
        self.lbl_lang.setText("🌐  " + self.loc.get("lbl_language"))
        self.lbl_theme.setText("🎨  " + self.loc.get("lbl_theme"))
        self.btn_en.setText("🇬🇧  " + self.loc.get("btn_lang_en"))
        self.btn_vn.setText("🇻🇳  " + self.loc.get("btn_lang_vn"))
        self.btn_dark.setText("🌙  " + self.loc.get("btn_theme_dark"))
        self.btn_light.setText("☀️  " + self.loc.get("btn_theme_light"))
        self._lang = self.loc.current_lang
        self._refresh_lang_btns()


    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.lbl_lang.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.lbl_theme.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.btn_back.apply_theme()
        self._refresh_lang_btns()

# ── Screen: Session Creator ───────────────────
class SessionCreatorScreen(QWidget):
    back_signal = pyqtSignal()

    def __init__(self, session_manager, loc_manager, cem=None):
        super().__init__()
        self.session_manager = session_manager
        self.loc = loc_manager
        self.cem = cem
        self.current_exercises = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(18)

        # Header
        hdr = QHBoxLayout()
        self.btn_back = BackButton(); self.btn_back.setFixedWidth(140); self.btn_back.setMinimumHeight(44)
        self.btn_back.clicked.connect(self.back_signal.emit)
        hdr.addWidget(self.btn_back); hdr.addStretch()
        self.title = QLabel()
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self.title); hdr.addStretch(); hdr.addSpacing(140)
        layout.addLayout(hdr)

        # Session name
        self.lbl_name = QLabel()
        self.lbl_name.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        layout.addWidget(self.lbl_name)
        self.name_input = QLineEdit(); self.name_input.setMinimumHeight(48); self.name_input.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.name_input)

        # Add exercise card
        self.adder = make_card(); al = QHBoxLayout(self.adder)
        al.setContentsMargins(16, 12, 16, 12); al.setSpacing(10)
        self.combo_ex = QComboBox(); self.combo_ex.setMinimumHeight(46); self.combo_ex.setFont(QFont("Segoe UI", 16))
        self.combo_ex.setStyleSheet(f"QComboBox{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_PRI']};border:1px solid {Theme.t['BORDER']};border-radius:8px;padding:0 10px;}} QComboBox:focus{{border-color:{Theme.t['PRI']};}} QComboBox::drop-down{{border:0px;}}")
        self.refresh_exercises()
        self.spin_sets = QSpinBox(); self.spin_sets.setRange(1, 10); self.spin_sets.setValue(3); self.spin_sets.setMinimumHeight(46); self.spin_sets.setFixedWidth(130); self.spin_sets.setFont(QFont("Segoe UI", 16))
        self.spin_sets.setStyleSheet(f"QSpinBox{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_PRI']};border:1px solid {Theme.t['BORDER']};border-radius:8px;padding:0 10px;}} QSpinBox:focus{{border-color:{Theme.t['PRI']};}}")
        self.spin_reps = QSpinBox(); self.spin_reps.setRange(1, 100); self.spin_reps.setValue(10); self.spin_reps.setMinimumHeight(46); self.spin_reps.setFixedWidth(130); self.spin_reps.setFont(QFont("Segoe UI", 16))
        self.spin_reps.setStyleSheet(f"QSpinBox{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_PRI']};border:1px solid {Theme.t['BORDER']};border-radius:8px;padding:0 10px;}} QSpinBox:focus{{border-color:{Theme.t['PRI']};}}")
        self.btn_add = AddButton(); self.btn_add.setMinimumHeight(46); self.btn_add.setFixedWidth(140)
        self.btn_add.clicked.connect(self.add_exercise)
        al.addWidget(self.combo_ex, 3); al.addWidget(self.spin_sets, 1); al.addWidget(self.spin_reps, 1); al.addWidget(self.btn_add)
        layout.addWidget(self.adder)

        # List
        self.lbl_list = QLabel()
        self.lbl_list.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        layout.addWidget(self.lbl_list)
        self.list_exercises = QListWidget(); self.list_exercises.setSpacing(2); self.list_exercises.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.list_exercises)

        self.btn_save = PrimaryButton(); self.btn_save.setMinimumHeight(52)
        self.btn_save.clicked.connect(self.save_session)
        layout.addWidget(self.btn_save)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.title.setText(self.loc.get("title_create"))
        self.btn_back.setText("  " + self.loc.get("back"))
        self.lbl_name.setText(self.loc.get("lbl_session_name"))
        self.name_input.setPlaceholderText(self.loc.get("ph_session_name"))
        self.spin_sets.setPrefix(self.loc.get("lbl_set") + " ")
        self.spin_reps.setPrefix(self.loc.get("lbl_reps") + " ")
        self.btn_add.setText("  " + self.loc.get("btn_add"))
        self.lbl_list.setText(self.loc.get("lbl_session_exercises"))
        self.btn_save.setText("💾  " + self.loc.get("btn_save_session"))

    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.lbl_name.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.lbl_list.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.adder.setStyleSheet(f"QFrame{{background:{Theme.t['BG_CARD']};border:1px solid {Theme.t['BORDER']};border-radius:14px;}}")
        if hasattr(self.btn_back, 'apply_theme'): self.btn_back.apply_theme()
        # Updates to the list items will happen on recreate, but we don't rebuild them automatically here.
        # For a full theme change, they could be rebuilt.

    def refresh_exercises(self):
        self.combo_ex.clear()
        self.combo_ex.addItems(["Squat", "Bicep Curl", "Push Up"])
        if hasattr(self, 'cem') and self.cem:
            self.combo_ex.addItems(list(self.cem.get_custom_rules().keys()))

    def add_exercise(self):
        name = self.combo_ex.currentText()
        sets = self.spin_sets.value(); reps = self.spin_reps.value()
        self.current_exercises.append({"name": name, "sets": sets, "reps": reps})
        icon = "🏋️" if name == "Squat" else "💪"
        # Widget row
        row_w = QFrame()
        row_w.setStyleSheet(f"background: {Theme.t['BG_CARD2']}; border-radius: 1px;")
        rh = QHBoxLayout(row_w)
        rh.setContentsMargins(12, 8, 12, 8)  # Even padding all around
        set_word  = self.loc.get('lbl_set').rstrip(':').rstrip()
        reps_word = self.loc.get('lbl_reps').rstrip(':').rstrip()
        lbl = QLabel(f"{icon}  {name}  —  {sets} {set_word} × {reps} {reps_word}")
        lbl.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};font-weight:600;background:transparent;font-size:16px;")
        del_btn = SmallIconButton("✕")
        #rh.addWidget(lbl, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        rh.addWidget(lbl)
        #rh.addWidget(del_btn, 1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        rh.addWidget(del_btn)
        idx = len(self.current_exercises) - 1
        del_btn.clicked.connect(lambda _, i=idx: self.remove_exercise(i))
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 64))
        self.list_exercises.addItem(item)
        self.list_exercises.setItemWidget(item, row_w)

    def remove_exercise(self, index):
        if 0 <= index < len(self.current_exercises):
            self.current_exercises.pop(index)
            self.list_exercises.takeItem(index)
            self._rebind_deletes()

    def _rebind_deletes(self):
        for i in range(self.list_exercises.count()):
            w = self.list_exercises.itemWidget(self.list_exercises.item(i))
            if w:
                for b in w.findChildren(SmallIconButton):
                    try: b.clicked.disconnect()
                    except: pass
                    b.clicked.connect(lambda _, idx=i: self.remove_exercise(idx))

    def save_session(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, self.loc.get("msg_error"), self.loc.get("msg_enter_name")); return
        if not self.current_exercises:
            QMessageBox.warning(self, self.loc.get("msg_error"), self.loc.get("msg_add_one")); return
        self.session_manager.save_session(name, self.current_exercises)
        QMessageBox.information(self, self.loc.get("msg_success"), f"{self.loc.get('msg_saved')} ({name})")
        self.list_exercises.clear(); self.current_exercises = []; self.name_input.clear()
        self.back_signal.emit()

# ── Screen: Session Selection ─────────────────
class SessionSelectionScreen(QWidget):
    back_signal = pyqtSignal()
    session_selected_signal = pyqtSignal(list, str)

    def __init__(self, session_manager, loc_manager):
        super().__init__()
        self.session_manager = session_manager
        self.loc = loc_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(20)
        hdr = QHBoxLayout()
        self.btn_back = BackButton(); self.btn_back.setFixedWidth(140); self.btn_back.setMinimumHeight(44)
        self.btn_back.clicked.connect(self.back_signal.emit)
        hdr.addWidget(self.btn_back); hdr.addStretch()
        self.title = QLabel()
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self.title); hdr.addStretch(); hdr.addSpacing(140)
        layout.addLayout(hdr)
        self.list_sessions = QListWidget(); self.list_sessions.setSpacing(3)
        self.list_sessions.itemDoubleClicked.connect(self.on_session_picked)
        layout.addWidget(self.list_sessions)
        self.btn_start = PrimaryButton(); self.btn_start.setMinimumHeight(52)
        self.btn_start.clicked.connect(self.on_start_click)
        layout.addWidget(self.btn_start)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.title.setText(self.loc.get("title_select"))
        self.btn_back.setText("  " + self.loc.get("back"))
        self.btn_start.setText("▶  " + self.loc.get("btn_start_selected"))
        self.refresh_sessions()

    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        if hasattr(self.btn_back, 'apply_theme'): self.btn_back.apply_theme()
        self.refresh_sessions()

    def refresh_sessions(self):
        self.list_sessions.clear()
        sessions = self.session_manager.get_sessions()
        if not sessions:
            placeholder = QListWidgetItem("  📭  No sessions yet. Create one first!")
            placeholder.setForeground(QColor(Theme.t['TEXT_MUTED']))
            placeholder.setFont(QFont("Segoe UI", 16))
            self.list_sessions.addItem(placeholder)
            return
        for sname, exercises in sessions.items():
            count = len(exercises)
            summary = ", ".join([e['name'] for e in exercises[:3]])
            if count > 3: summary += "…"
            row_w = QWidget(); row_w.setStyleSheet("background:transparent;")
            rh = QHBoxLayout(row_w); rh.setContentsMargins(14, 10, 14, 10)
            info = QVBoxLayout()
            lbl_n = QLabel(sname); lbl_n.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            lbl_n.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};background:transparent;")
            lbl_s = QLabel(f"{count} exercises  ·  {summary}")
            lbl_s.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};font-size:14px;background:transparent;")
            info.addWidget(lbl_n); info.addWidget(lbl_s)
            play = PrimaryButton("▶"); play.setFixedSize(48, 48)
            play.clicked.connect(lambda _, n=sname: self._launch(n))
            rh.addLayout(info, 1); rh.addWidget(play)
            item = QListWidgetItem(); item.setSizeHint(QSize(0, 95))
            self.list_sessions.addItem(item)
            self.list_sessions.setItemWidget(item, row_w)

    def _launch(self, name):
        exs = self.session_manager.get_session(name)
        if exs: self.session_selected_signal.emit(exs, name)

    def _selected_name(self):
        item = self.list_sessions.currentItem()
        if not item: return None
        w = self.list_sessions.itemWidget(item)
        if not w: return None
        labels = w.findChildren(QLabel)
        return labels[0].text() if labels else None

    def on_start_click(self):
        n = self._selected_name()
        if n: self._launch(n)

    def on_session_picked(self, item):
        self.on_start_click()

# ── Screen: Planner ───────────────────────────
class PlannerScreen(QWidget):
    back_signal = pyqtSignal()

    BODY_PARTS = [
        ("🏋️", "Full Body",   "Toàn Thân",  "full_body"),
        ("💪", "Upper Body",  "Thân Trên",  "upper_body"),
        ("🦵", "Lower Body",  "Thân Dưới",  "lower_body"),
        ("🔥", "Core",        "Cơ Lõi",     "core"),
        ("🏃", "Cardio",      "Cardio",      "cardio"),
    ]

    def __init__(self, loc_manager):
        super().__init__()
        self.planner = WorkoutPlanner()
        self.loc = loc_manager
        self._selected_parts = {"full_body"}   # default selection
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(20)
        hdr = QHBoxLayout()
        self.btn_back = BackButton(); self.btn_back.setFixedWidth(140); self.btn_back.setMinimumHeight(44)
        self.btn_back.clicked.connect(self.back_signal.emit)
        hdr.addWidget(self.btn_back); hdr.addStretch()
        self.title = QLabel()
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self.title); hdr.addStretch(); hdr.addSpacing(140)
        layout.addLayout(hdr)

        # ── Body Part Selector ────────────────────
        self.fc = make_card(); fl = QVBoxLayout(self.fc)
        fl.setContentsMargins(24, 20, 24, 20); fl.setSpacing(14)

        self.lbl_focus = QLabel()
        self.lbl_focus.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        fl.addWidget(self.lbl_focus)

        self.part_btns = {}  # key -> QPushButton
        part_row = QHBoxLayout(); part_row.setSpacing(10)
        for icon, label_en, label_vn, key in self.BODY_PARTS:
            btn = QPushButton(f"{icon}  {label_en}")
            btn.setCheckable(True)
            btn.setChecked(key == "full_body")
            btn.setMinimumHeight(44)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            btn.clicked.connect(lambda checked, k=key: self._toggle_part(k))
            self.part_btns[key] = btn
            part_row.addWidget(btn)
        fl.addLayout(part_row)

        # ── Settings row ─────────────────────────
        r1 = QHBoxLayout()
        self.lbl_mins = QLabel(); self.lbl_mins.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.input_minutes = QLineEdit(); self.input_minutes.setPlaceholderText("e.g. 30"); self.input_minutes.setMinimumHeight(46); self.input_minutes.setFont(QFont("Segoe UI", 16))
        r1.addWidget(self.lbl_mins, 1); r1.addWidget(self.input_minutes, 2)
        r2 = QHBoxLayout()
        self.lbl_days = QLabel(); self.lbl_days.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.input_days = QLineEdit(); self.input_days.setPlaceholderText("e.g. 3"); self.input_days.setMinimumHeight(46); self.input_days.setFont(QFont("Segoe UI", 16))
        r2.addWidget(self.lbl_days, 1); r2.addWidget(self.input_days, 2)
        self.btn_generate = PrimaryButton(); self.btn_generate.setMinimumHeight(52)
        self.btn_generate.clicked.connect(self.generate_plan)
        fl.addLayout(r1); fl.addLayout(r2); fl.addWidget(self.btn_generate)
        layout.addWidget(self.fc)
        self.result_area = QTextEdit(); self.result_area.setReadOnly(True)
        self.result_area.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.result_area, 1)
        self._refresh_part_btns()
        self.retranslate_ui()

    def _toggle_part(self, key):
        if key in self._selected_parts:
            # Don't allow deselecting everything
            if len(self._selected_parts) > 1:
                self._selected_parts.discard(key)
        else:
            self._selected_parts.add(key)
        self._refresh_part_btns()

    def _refresh_part_btns(self):
        active_ss = (
            f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {Theme.t['PRI']},stop:1 {Theme.t['PRI_DARK']});"
            f"color:white;border:none;border-radius:10px;padding:8px 14px;}}"
        )
        inactive_ss = (
            f"QPushButton{{background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_SEC']};"
            f"border:1px solid {Theme.t['BORDER']};border-radius:10px;padding:8px 14px;}}"
            f"QPushButton:hover{{border-color:{Theme.t['PRI']};color:{Theme.t['PRI_LIGHT']};}}"
        )
        for key, btn in self.part_btns.items():
            btn.setChecked(key in self._selected_parts)
            btn.setStyleSheet(active_ss if key in self._selected_parts else inactive_ss)

    def retranslate_ui(self):
        self.title.setText(self.loc.get("title_planner"))
        self.btn_back.setText("  " + self.loc.get("back"))
        self.lbl_focus.setText("🎯  " + self.loc.get("lbl_focus"))
        self.lbl_mins.setText("⏱  " + self.loc.get("lbl_mins"))
        self.lbl_days.setText("📅  " + self.loc.get("lbl_days"))
        self.btn_generate.setText("⚡  " + self.loc.get("btn_generate"))
        self.result_area.setPlaceholderText(self.loc.get("ph_result"))
        self._retranslate_part_btns()

    def _retranslate_part_btns(self):
        lang = self.loc.current_lang
        for icon, label_en, label_vn, key in self.BODY_PARTS:
            label = label_vn if lang == "vn" else label_en
            self.part_btns[key].setText(f"{icon}  {label}")

    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.lbl_focus.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.lbl_mins.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.lbl_days.setStyleSheet(f"color:{Theme.t['TEXT_SEC']};font-weight:600;font-size:16px;")
        self.fc.setStyleSheet(f"QFrame{{background:{Theme.t['BG_CARD']};border:1px solid {Theme.t['BORDER']};border-radius:14px;}}")
        self._refresh_part_btns()
        if hasattr(self.btn_back, 'apply_theme'): self.btn_back.apply_theme()

    def generate_plan(self):
        try:
            mins = int(self.input_minutes.text())
            days = int(self.input_days.text())
            lang = self.loc.current_lang
            plan = self.planner.create_plan(mins, days, list(self._selected_parts), lang=lang)
            self.result_area.setText(plan)
        except ValueError:
            err = "⚠️  Vui lòng nhập số hợp lệ." if self.loc.current_lang == "vn" else "⚠️  Please enter valid numbers."
            self.result_area.setText(err)

# ── Screen: Workout ───────────────────────────
class WorkoutScreen(QWidget):
    back_signal = pyqtSignal()

    def __init__(self, loc_manager, cem=None):
        super().__init__()
        self.loc = loc_manager
        self.cem = cem
        self.camera = None
        self.pose_estimator = PoseEstimator()
        self.evaluator = PostureEvaluator()
        self.rep_counter = RepCounter()
        self.feedback_sys = FeedbackSystem()
        self.scorer = Scorer()
        self.is_running = False
        self.exercise_queue = []
        self.current_ex_index = 0
        self.current_exercise_data = None
        self.current_rules = None
        self.current_set_count = 1
        self.target_sets = 3
        self.target_reps = 10
        self._last_count = 0
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def init_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(16)

        # ── Video side
        vc = QVBoxLayout()
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet(f"background:#050510;border:1px solid {Theme.t['BORDER']};border-radius:16px;color:{Theme.t['TEXT_MUTED']};font-size:16px;")
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        vc.addWidget(self.video_label)
        main.addLayout(vc, 2)

        # ── Control panel
        self.cp = QFrame()
        self.cp.setStyleSheet(f"QFrame{{background:{Theme.t['BG_SURFACE']};border:1px solid {Theme.t['BORDER']};border-radius:16px;}}")
        cl = QVBoxLayout(self.cp)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        self.btn_back = DangerButton()
        self.btn_back.setMinimumHeight(40)
        self.btn_back.clicked.connect(self.stop_and_exit)
        cl.addWidget(self.btn_back)

        self.title_label = QLabel()
        self.title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.addWidget(self.title_label)

        # Exercise info card
        self.ec = make_card(); el = QVBoxLayout(self.ec)
        el.setContentsMargins(16, 14, 16, 14); el.setSpacing(5)
        self.lbl_exercise_name = QLabel()
        self.lbl_exercise_name.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.lbl_exercise_name.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};background:transparent;")
        el.addWidget(self.lbl_exercise_name)
        self.lbl_set_info = QLabel()
        self.lbl_set_info.setStyleSheet(f"color:{Theme.t['SEC']};font-size:16px;font-weight:600;background:transparent;")
        el.addWidget(self.lbl_set_info)
        self.lbl_progress = QLabel()
        self.lbl_progress.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};font-size:14px;background:transparent;")
        el.addWidget(self.lbl_progress)
        self.set_progress_bar = QProgressBar()
        self.set_progress_bar.setRange(0, 100); self.set_progress_bar.setValue(0)
        self.set_progress_bar.setFixedHeight(12); self.set_progress_bar.setTextVisible(False)
        el.addWidget(self.set_progress_bar)
        cl.addWidget(self.ec)

        # Camera buttons
        self.btn_start = PrimaryButton()
        self.btn_start.setMinimumHeight(52)
        self.btn_start.clicked.connect(self.toggle_camera)
        cl.addWidget(self.btn_start)

        self.btn_next = SecondaryButton()
        self.btn_next.setMinimumHeight(52)
        self.btn_next.clicked.connect(self.next_exercise)
        cl.addWidget(self.btn_next)

        # Stats card
        self.sc = make_card(); sl = QVBoxLayout(self.sc)
        sl.setContentsMargins(16, 14, 16, 14); sl.setSpacing(8)
        self.stats_title = QLabel("📊  Live Stats")
        self.stats_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.stats_title.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        sl.addWidget(self.stats_title)

        self.lbl_reps = QLabel("0")
        self.lbl_reps.setFont(QFont("Segoe UI", 52, QFont.Weight.Black))
        self.lbl_reps.setStyleSheet(f"color:{Theme.t['SEC']};background:transparent;")
        self.lbl_reps.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sl.addWidget(self.lbl_reps)
        self.reps_hint = QLabel("reps completed")
        self.reps_hint.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};font-size:14px;background:transparent;")
        self.reps_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sl.addWidget(self.reps_hint)

        row_state = QHBoxLayout()
        self.state_lbl = QLabel("State:"); self.state_lbl.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;font-size:16px;")
        self.lbl_state = QLabel("WAITING")
        self.lbl_state.setStyleSheet(f"background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_SEC']};border-radius:8px;padding:4px 12px;font-weight:700;font-size:16px;")
        row_state.addWidget(self.state_lbl); row_state.addWidget(self.lbl_state); row_state.addStretch()
        sl.addLayout(row_state)

        row_score = QHBoxLayout()
        self.score_lbl = QLabel("Score:"); self.score_lbl.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;font-size:16px;")
        self.lbl_score = QLabel("0")
        self.lbl_score.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_score.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        row_score.addWidget(self.score_lbl); row_score.addWidget(self.lbl_score); row_score.addStretch()
        sl.addLayout(row_score)

        self.lbl_feedback = QLabel()
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_feedback("neutral", "")
        sl.addWidget(self.lbl_feedback)
        cl.addWidget(self.sc)
        cl.addStretch()
        main.addWidget(self.cp, 1)
        self.retranslate_ui()

    def apply_theme(self):
        self.video_label.setStyleSheet(f"background:#050510;border:1px solid {Theme.t['BORDER']};border-radius:16px;color:{Theme.t['TEXT_MUTED']};font-size:16px;")
        self.cp.setStyleSheet(f"QFrame{{background:{Theme.t['BG_SURFACE']};border:1px solid {Theme.t['BORDER']};border-radius:16px;}}")
        self.title_label.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        self.ec.setStyleSheet(f"QFrame{{background:{Theme.t['BG_CARD']};border:1px solid {Theme.t['BORDER']};border-radius:14px;}}")
        self.lbl_exercise_name.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};background:transparent;")
        self.lbl_set_info.setStyleSheet(f"color:{Theme.t['SEC']};font-size:16px;font-weight:600;background:transparent;")
        self.lbl_progress.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};font-size:14px;background:transparent;")
        self.sc.setStyleSheet(f"QFrame{{background:{Theme.t['BG_CARD']};border:1px solid {Theme.t['BORDER']};border-radius:14px;}}")
        self.stats_title.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        self.lbl_reps.setStyleSheet(f"color:{Theme.t['SEC']};background:transparent;")
        self.reps_hint.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};font-size:14px;background:transparent;")
        self.state_lbl.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;font-size:16px;")
        self.lbl_state.setStyleSheet(f"background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_SEC']};border-radius:8px;padding:4px 12px;font-weight:700;font-size:16px;")
        self.score_lbl.setStyleSheet(f"color:{Theme.t['TEXT_MUTED']};background:transparent;font-size:16px;")
        self.lbl_score.setStyleSheet(f"color:{Theme.t['PRI_LIGHT']};background:transparent;")
        self._set_feedback("neutral", "") # Let it reset color to theme
        if hasattr(self.btn_back, 'apply_theme'): self.btn_back.apply_theme()

    # ── Helpers ────────────────────────────────
    def _set_state_badge(self, text, color, bg):
        self.lbl_state.setText(text)
        self.lbl_state.setStyleSheet(f"background:{bg};color:{color};border-radius:8px;padding:4px 12px;font-weight:700;font-size:16px;")

    def _set_feedback(self, mode, text):
        if mode == "good":
            style = f"color:{Theme.t['SEC']};background:rgba(0,212,180,0.12);border:1px solid rgba(0,212,180,0.4);"
        elif mode == "bad":
            style = f"color:{Theme.t['DANGER']};background:rgba(255,77,109,0.12);border:1px solid rgba(255,77,109,0.4);"
        else:
            style = f"color:{Theme.t['TEXT_SEC']};background:rgba(255,255,255,0.04);border:1px solid {Theme.t['BORDER']};"
        self.lbl_feedback.setStyleSheet(f"{style}border-radius:10px;padding:8px 12px;font-weight:bold;font-size:16px;")
        if text: self.lbl_feedback.setText(text)

    def _pop_reps(self):
        self.lbl_reps.setFont(QFont("Segoe UI", 60, QFont.Weight.Black))
        QTimer.singleShot(160, lambda: self.lbl_reps.setFont(QFont("Segoe UI", 52, QFont.Weight.Black)))

    def retranslate_ui(self):
        self.btn_back.setText("✕  " + self.loc.get("end_session"))
        self.title_label.setText(self.loc.get("title_workout"))
        if self.camera is None:
            self.video_label.setText(self.loc.get("cam_stopped"))
            self.btn_start.setText("📷  " + self.loc.get("btn_start_cam"))
        else:
            self.btn_start.setText("⏹  " + self.loc.get("btn_stop_cam"))
        if self.current_exercise_data:
            self.update_set_display()
            self.lbl_exercise_name.setText(self.current_exercise_data['name'])
        else:
            self.lbl_exercise_name.setText("No exercise loaded")
            self.lbl_set_info.setText("Set 0 / 0")
            self.lbl_reps.setText("0")
        self._set_state_badge("WAITING", Theme.t['TEXT_MUTED'], Theme.t['BG_CARD2'])
        self.lbl_score.setText("0")
        self._set_feedback("neutral", self.loc.get("status_ready"))
        self.btn_next.setText(("⏭  " + self.loc.get("btn_next_ex")) if len(self.exercise_queue) > self.current_ex_index + 1 else ("✅  " + self.loc.get("btn_finish_workout")))

    def start_session(self, exercises, name="Custom"):
        self.exercise_queue = exercises
        self.current_ex_index = 0
        self.title_label.setText(f"{self.loc.get('title_workout')}: {name}")
        self.load_current_exercise()

    def load_current_exercise(self):
        if 0 <= self.current_ex_index < len(self.exercise_queue):
            self.current_exercise_data = self.exercise_queue[self.current_ex_index]
            ex_name = self.current_exercise_data['name']
            self.target_sets = self.current_exercise_data.get('sets', 3)
            self.target_reps = self.current_exercise_data.get('reps', 10)
            self.current_set_count = 1
            self._last_count = 0
            icon = "🏋️ " if ex_name == "Squat" else "💪 "
            self.lbl_exercise_name.setText(icon + ex_name)
            self.lbl_progress.setText(f"Exercise {self.current_ex_index + 1} / {len(self.exercise_queue)}")
            self.update_set_display()
            if ex_name == "Squat":
                self.current_rules = ExerciseRules.get_squat_rules()
            elif ex_name == "Push Up":
                self.current_rules = ExerciseRules.get_push_up_rules()
            elif ex_name == "Bicep Curl":
                self.current_rules = ExerciseRules.get_curl_rules()
            else:
                if self.cem:
                    self.current_rules = self.cem.get_custom_rules().get(ex_name)
                else:
                    self.current_rules = None
            
            if not self.current_rules:
                QMessageBox.warning(self, "Error", f"Rules for {ex_name} not found.")
                return

            self.rep_counter.set_exercise(self.current_rules)
            self.scorer.reset()
            self.lbl_score.setText("0")
            self._set_state_badge("WAITING", Theme.t['TEXT_MUTED'], Theme.t['BG_CARD2'])
            self._set_feedback("neutral", self.loc.get("status_ready"))
            more = len(self.exercise_queue) > self.current_ex_index + 1
            self.btn_next.setText("⏭  " + self.loc.get("btn_next_ex") if more else "✅  " + self.loc.get("btn_finish_workout"))
            self.btn_next.setEnabled(True)
        else:
            self.lbl_exercise_name.setText(self.loc.get("msg_workout_done"))
            self.btn_next.setEnabled(False)

    def update_set_display(self):
        self.lbl_set_info.setText(f"Set {self.current_set_count} / {self.target_sets}")
        self.lbl_reps.setText(f"0 / {self.target_reps}")
        self.set_progress_bar.setValue(0)

    def next_exercise(self):
        self.current_ex_index += 1
        if self.current_ex_index < len(self.exercise_queue):
            self.load_current_exercise()
        else:
            QMessageBox.information(self, self.loc.get("msg_finished"), self.loc.get("msg_workout_done"))
            self.stop_and_exit()

    def toggle_camera(self):
        if not self.is_running:
            try:
                self.camera = Camera()
                self.timer.start(30)
                self.btn_start.setText("⏹  " + self.loc.get("btn_stop_cam"))
                self.btn_start.setStyleSheet(f"QPushButton{{background:rgba(255,77,109,0.15);color:{Theme.t['DANGER']};border:1px solid rgba(255,77,109,0.4);border-radius:10px;padding:10px 20px;font-weight:700;font-size:13px;}} QPushButton:hover{{background:{Theme.t['DANGER']};color:white;}}")
                self.is_running = True
            except Exception as e:
                self._set_feedback("bad", f"{self.loc.get('cam_error')}: {e}")
        else:
            self.stop_camera()

    def stop_camera(self):
        self.timer.stop()
        if self.camera:
            self.camera.release(); self.camera = None
        self.video_label.clear()
        self.video_label.setText(self.loc.get("cam_stopped"))
        self.btn_start.setText("📷  " + self.loc.get("btn_start_cam"))
        self.btn_start.setStyleSheet("")  # restore global style
        self.is_running = False

    def stop_and_exit(self):
        self.stop_camera()
        self.back_signal.emit()

    def update_frame(self):
        if not self.camera: return
        frame = self.camera.get_frame()
        if frame is None: return
        results = self.pose_estimator.process_frame(frame)
        frame = self.pose_estimator.draw_landmarks(frame, results)
        landmarks = self.pose_estimator.get_landmarks(results)
        if landmarks and self.current_rules:
            try:
                joints = self.current_rules["landmarks"]
                p1n, p2n, p3n = self.current_rules["joint_angles"]
                def gp(n): return [landmarks[joints[n]].x, landmarks[joints[n]].y]
                angle = calculate_angle(gp(p1n), gp(p2n), gp(p3n))
                if self.current_exercise_data['name'] == "Squat":
                    good, msg = self.evaluator.check_squat(landmarks)
                else:
                    good, msg = self.evaluator.check_curl(landmarks)
                self.scorer.update(good)
                if good:
                    count, state = self.rep_counter.process(angle)
                    if state == "COUNT":
                        self.feedback_sys.play_audio(str(count)); state = "UP"
                    if count != self._last_count:
                        self._last_count = count; self._pop_reps()
                    self.lbl_reps.setText(f"{count} / {self.target_reps}")
                    self._set_state_badge(state, Theme.t['SEC'] if state == "UP" else Theme.t['TEXT_SEC'], Theme.t['BG_CARD2'])
                    if count >= self.target_reps:
                        self.complete_set(); return
                    self._set_feedback("good", self.loc.get("status_good"))
                else:
                    self._set_feedback("bad", msg)
                self.lbl_score.setText(str(self.scorer.get_score()))
            except Exception:
                pass
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(
            QPixmap.fromImage(qt_img).scaled(
                self.video_label.width(), self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio))

    def complete_set(self):
        self.rep_counter.count = 0
        self.feedback_sys.play_audio(self.loc.get("msg_set_complete"))
        self.current_set_count += 1
        if self.current_set_count > self.target_sets:
            self.feedback_sys.play_audio(self.loc.get("msg_ex_complete"))
            QMessageBox.information(self, self.loc.get("msg_finished"),
                                    f"{self.current_exercise_data['name']} {self.loc.get('msg_finished')}!")
            self.next_exercise()
        else:
            QMessageBox.information(self, self.loc.get("msg_set_complete"),
                                    f"{self.loc.get('msg_set_complete')} {self.loc.get('msg_take_rest')}")
            self.update_set_display()

# ── Screen: Custom Exercise ───────────────────
class AnalyzerThread(QThread):
    finished_signal = pyqtSignal(object)
    error_signal = pyqtSignal(str)
    
    def __init__(self, analyzer, path, name):
        super().__init__()
        self.analyzer = analyzer
        self.path = path
        self.name = name
        
    def run(self):
        try:
            res = self.analyzer.analyze_video(self.path, self.name)
            self.finished_signal.emit(res)
        except Exception as e:
            self.error_signal.emit(str(e))

class CustomExerciseScreen(QWidget):
    back_signal = pyqtSignal()
    
    def __init__(self, cem, analyzer, loc_manager):
        super().__init__()
        self.cem = cem
        self.analyzer = analyzer
        self.loc = loc_manager
        self.setAcceptDrops(True)
        self.video_path = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(18)

        # Header
        hdr = QHBoxLayout()
        self.btn_back = BackButton(); self.btn_back.setFixedWidth(140); self.btn_back.setMinimumHeight(44)
        self.btn_back.clicked.connect(self.back_signal.emit)
        hdr.addWidget(self.btn_back); hdr.addStretch()
        self.title = QLabel("Create Custom Exercise")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self.title); hdr.addStretch(); hdr.addSpacing(140)
        layout.addLayout(hdr)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Exercise Name (e.g. Jumping Jacks)")
        self.name_input.setMinimumHeight(48)
        self.name_input.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.name_input)
        
        # Drop Zone
        self.drop_zone = QLabel("Drag & Drop Video Here\nor Click to Browse")
        self.drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_zone.setFont(QFont("Segoe UI", 16))
        self.drop_zone.setStyleSheet(f"background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_MUTED']};border:2px dashed {Theme.t['BORDER']};border-radius:14px;")
        self.drop_zone.setMinimumHeight(200)
        layout.addWidget(self.drop_zone)
        
        # We need a hidden button that covers the drop zone to allow click
        self.btn_browse = QPushButton(self.drop_zone)
        self.btn_browse.setStyleSheet("background:transparent;border:none;")
        self.btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_file)
        
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet(f"color:{Theme.t['SEC']};font-size:16px;font-weight:600;")
        layout.addWidget(self.lbl_status)
        
        layout.addStretch()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_browse.resize(self.drop_zone.size())

    def apply_theme(self):
        self.title.setStyleSheet(f"color:{Theme.t['TEXT_PRI']};")
        self.drop_zone.setStyleSheet(f"background:{Theme.t['BG_CARD2']};color:{Theme.t['TEXT_MUTED']};border:2px dashed {Theme.t['BORDER']};border-radius:14px;")
        if hasattr(self.btn_back, 'apply_theme'): self.btn_back.apply_theme()
        
    def retranslate_ui(self):
        self.title.setText(self.loc.get("btn_custom_ex") if self.loc.get("btn_custom_ex") != "btn_custom_ex" else "Custom Exercise")
        self.btn_back.setText("  " + self.loc.get("back"))
        self.name_input.setPlaceholderText("Exercise Name")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        self.video_path = url.toLocalFile()
        self.process_video()

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if path:
            self.video_path = path
            self.process_video()

    def process_video(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter an exercise name first.")
            return

        if not self.video_path:
            QMessageBox.warning(self, "Error", "Please select a video file first.")
            return
        
        filename = str(self.video_path).replace("\\", "/").split("/")[-1]
        self.drop_zone.setText(f"Selected: {filename}\nAnalyzing... Please wait.")
        self.lbl_status.setText("Analyzing...")
        self.btn_browse.setEnabled(False)
        self.setAcceptDrops(False)
        
        self.thread = AnalyzerThread(self.analyzer, self.video_path, name)
        self.thread.finished_signal.connect(self.on_analysis_complete)
        self.thread.error_signal.connect(self.on_analysis_error)
        self.thread.start()
        
    def on_analysis_complete(self, rule):
        self.btn_browse.setEnabled(True)
        self.setAcceptDrops(True)
        self.drop_zone.setText("Drag & Drop Video Here\nor Click to Browse")
        
        if self.cem.save_custom_exercise(rule):
            self.lbl_status.setText(f"Success! {rule['name']} tracked using {rule['joint_angles']}.")
            QMessageBox.information(self, "Success", "Custom exercise saved successfully!")
            self.name_input.clear()
            self.video_path = None
            self.back_signal.emit()
        else:
            self.lbl_status.setText("Failed to save.")
            
    def on_analysis_error(self, err):
        self.btn_browse.setEnabled(True)
        self.setAcceptDrops(True)
        self.drop_zone.setText("Drag & Drop Video Here\nor Click to Browse")
        self.lbl_status.setText(f"Error: {err}")
        QMessageBox.warning(self, "Error", str(err))

# ── Main Window ───────────────────────────────
class FitnessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loc_manager = LocalizationManager(default_lang='vn')
        self.session_manager = SessionManager()
        self.cem = CustomExerciseManager()
        self.analyzer = VideoAnalyzer()
        
        self.setWindowTitle(self.loc_manager.get("app_title"))
        self.setGeometry(100, 100, 1100, 720)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(get_stylesheet())

        self.stack = AnimatedStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu            = MainMenu(self.loc_manager)
        self.workout_screen       = WorkoutScreen(self.loc_manager, self.cem)
        self.planner_screen       = PlannerScreen(self.loc_manager)
        self.session_create_screen= SessionCreatorScreen(self.session_manager, self.loc_manager, self.cem)
        self.session_select_screen= SessionSelectionScreen(self.session_manager, self.loc_manager)
        self.settings_screen      = SettingsScreen(self.loc_manager)
        self.custom_ex_screen     = CustomExerciseScreen(self.cem, self.analyzer, self.loc_manager)

        self.stack.addWidget(self.main_menu)              # 0
        self.stack.addWidget(self.workout_screen)         # 1
        self.stack.addWidget(self.planner_screen)         # 2
        self.stack.addWidget(self.session_create_screen)  # 3
        self.stack.addWidget(self.session_select_screen)  # 4
        self.stack.addWidget(self.settings_screen)        # 5
        self.stack.addWidget(self.custom_ex_screen)       # 6

        # Signals
        self.main_menu.start_workout_signal.connect(self.show_session_select)
        self.main_menu.create_session_signal.connect(self.show_session_create)
        self.main_menu.custom_ex_signal.connect(self.show_custom_ex)
        self.main_menu.planner_signal.connect(self.show_planner)
        self.main_menu.settings_signal.connect(self.show_settings)
        self.main_menu.exit_signal.connect(self.close)

        self.session_create_screen.back_signal.connect(self.show_menu)
        self.session_select_screen.back_signal.connect(self.show_menu)
        self.session_select_screen.session_selected_signal.connect(self.start_workout_session)
        self.planner_screen.back_signal.connect(self.show_menu)
        self.workout_screen.back_signal.connect(self.show_menu)
        self.settings_screen.back_signal.connect(self.show_menu)
        self.custom_ex_screen.back_signal.connect(self.show_home_update)
        
        self.settings_screen.lang_changed_signal.connect(self.change_language)
        self.settings_screen.theme_changed_signal.connect(self.change_theme)

    def change_theme(self, theme_name):
        Theme.current = theme_name
        Theme.t = THEMES[Theme.current]
        self.setStyleSheet(get_stylesheet())
        for screen in [self.main_menu, self.session_create_screen,
                       self.session_select_screen, self.planner_screen,
                       self.workout_screen, self.settings_screen, self.custom_ex_screen]:
            if hasattr(screen, 'apply_theme'):
                screen.apply_theme()

    def change_language(self, lang):
        self.loc_manager.set_language(lang)
        self.setWindowTitle(self.loc_manager.get("app_title"))
        for screen in [self.main_menu, self.session_create_screen,
                       self.session_select_screen, self.planner_screen,
                       self.workout_screen, self.settings_screen, self.custom_ex_screen]:
            if hasattr(screen, 'retranslate_ui'):
                screen.retranslate_ui()

    def show_menu(self):        
        self.stack.slide_to(0, "right")
        self.session_create_screen.refresh_exercises()
        
    def show_home_update(self): 
        self.stack.slide_to(0, "right")
        self.session_create_screen.refresh_exercises()
        
    def show_planner(self):     self.planner_screen.retranslate_ui();       self.stack.slide_to(2)
    def show_session_create(self): self.session_create_screen.retranslate_ui(); self.stack.slide_to(3)
    def show_session_select(self):
        self.session_select_screen.retranslate_ui()
        self.session_select_screen.refresh_sessions()
        self.stack.slide_to(4)
    def show_settings(self):    self.settings_screen.retranslate_ui();      self.stack.slide_to(5)
    def show_custom_ex(self):   self.custom_ex_screen.retranslate_ui();     self.stack.slide_to(6)

    def start_workout_session(self, exercises, name):
        if not exercises:
            QMessageBox.warning(self, self.loc_manager.get("msg_error"), self.loc_manager.get("msg_error"))
            return
        self.workout_screen.start_session(exercises, name)
        self.stack.slide_to(1)

    def closeEvent(self, event):
        self.workout_screen.stop_camera()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FitnessApp()
    window.show()
    sys.exit(app.exec())


