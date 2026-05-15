class Colors:
    BG_MAIN = "#1a1a2e"
    BG_CARD = "#16213e"
    BG_ALT = "#0f3460"
    BG_INPUT = "#0f1020"

    ACCENT = "#e94560"
    ACCENT_HOVER = "#ff5773"
    ACCENT_PRESSED = "#d13d55"

    SECONDARY = "#0f3460"
    SECONDARY_HOVER = "#1a4a80"

    PURPLE = "#533483"

    TEXT = "#e0e0e0"
    TEXT_WHITE = "#ffffff"
    TEXT_DIM = "#a0a0b0"
    TEXT_MUTED = "#888888"

    BORDER = "#333333"
    BORDER_LIGHT = "#444444"

    SCORE_PERFECT = "#4CAF50"
    SCORE_GOOD = "#2196F3"
    SCORE_NEUTRAL = "#9E9E9E"
    SCORE_BAD = "#FF9800"
    SCORE_CRITICAL = "#F44336"

    DANGER = "#d9534f"
    DANGER_HOVER = "#c9302c"

    MEDAL_COLORS = [ACCENT, PURPLE, SECONDARY]


class Styles:
    @staticmethod
    def colored_btn(bg, size="13px", padding="8px 16px"):
        return (
            f"background-color: {bg}; color: white; "
            f"font-size: {size}; font-weight: bold; "
            f"padding: {padding}; border: none; border-radius: 6px;"
        )

    @staticmethod
    def label_heading(color=None):
        if color is None:
            color = Colors.ACCENT
        return f"font-weight: bold; margin-top: 10px; color: {color};"

    @staticmethod
    def result_card(border_color):
        return f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 15px;
            }}
        """

    @staticmethod
    def text_style(size=13, color=None, bold=False, extra=""):
        if color is None:
            color = Colors.TEXT
        weight = "font-weight: bold; " if bold else ""
        return f"font-size: {size}px; {weight}color: {color};{' ' + extra if extra else ''}"
