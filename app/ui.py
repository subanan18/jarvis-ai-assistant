import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class JarvisOrb(QWidget):
    """Animated glowing orb for the JARVIS popup."""

    def __init__(self):
        super().__init__()
        self.animation_value = 0
        self.animation_direction = 1
        self.setMinimumSize(130, 130)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.animation_value += self.animation_direction
        if self.animation_value >= 20:
            self.animation_direction = -1
        elif self.animation_value <= 0:
            self.animation_direction = 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        centre_x = self.width() / 2
        centre_y = self.height() / 2
        pulse = self.animation_value / 2
        glow_radius = 48 + pulse

        gradient = QRadialGradient(centre_x, centre_y, glow_radius)
        gradient.setColorAt(0.0, QColor(60, 210, 255, 230))
        gradient.setColorAt(0.45, QColor(20, 130, 255, 180))
        gradient.setColorAt(1.0, QColor(0, 40, 120, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(centre_x - glow_radius),
            int(centre_y - glow_radius),
            int(glow_radius * 2),
            int(glow_radius * 2),
        )

        orb_radius = 32
        orb_gradient = QRadialGradient(
            centre_x - 8,
            centre_y - 8,
            orb_radius * 1.5,
        )
        orb_gradient.setColorAt(0.0, QColor(230, 255, 255))
        orb_gradient.setColorAt(0.3, QColor(80, 220, 255))
        orb_gradient.setColorAt(0.7, QColor(30, 100, 240))
        orb_gradient.setColorAt(1.0, QColor(10, 20, 70))
        painter.setBrush(orb_gradient)
        painter.setPen(QPen(QColor(130, 240, 255), 2))
        painter.drawEllipse(
            int(centre_x - orb_radius),
            int(centre_y - orb_radius),
            orb_radius * 2,
            orb_radius * 2,
        )

        painter.setBrush(Qt.BrushStyle.NoBrush)
        for index in range(3):
            wave_offset = (self.animation_value + index * 7) % 20
            wave_radius = 38 + wave_offset
            alpha = max(0, 150 - wave_offset * 7)
            painter.setPen(QPen(QColor(80, 220, 255, alpha), 2))
            painter.drawEllipse(
                int(centre_x - wave_radius),
                int(centre_y - wave_radius),
                int(wave_radius * 2),
                int(wave_radius * 2),
            )


class JarvisPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(330, 260)
        self.create_interface()
        self.position_window()

    def create_interface(self):
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet(
            """
            QWidget#container {
                background-color: rgba(8, 12, 28, 245);
                border: 1px solid rgba(70, 200, 255, 160);
                border-radius: 28px;
            }
            QLabel { background: transparent; }
            """
        )

        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 15, 25, 25)
        layout.setSpacing(3)
        self.orb = JarvisOrb()

        self.title_label = QLabel("JARVIS")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(
            "color: rgb(140, 235, 255); font-size: 22px; font-weight: 700;"
        )

        self.status_label = QLabel("Listening...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            "color: white; font-size: 17px; font-weight: 500;"
        )

        self.message_label = QLabel("How can I help you?")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet(
            "color: rgba(210, 225, 245, 190); font-size: 13px;"
        )

        layout.addWidget(self.orb, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.message_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

    def position_window(self):
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        screen_area = screen.availableGeometry()
        self.move(
            screen_area.right() - self.width() - 30,
            screen_area.bottom() - self.height() - 50,
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    popup = JarvisPopup()
    popup.show()
    popup.raise_()
    popup.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
