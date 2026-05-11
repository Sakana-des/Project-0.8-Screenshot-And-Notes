import sys
import re
import requests
from io import BytesIO
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QLineEdit, QFileDialog, QMessageBox, QColorDialog, QScrollArea)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage, QFont, QBrush
from PyQt5.QtCore import Qt, QPoint, QBuffer, QIODevice, QTimer, pyqtSignal, QRect

def upload_to_catbox(image_bytes):
    url = "https://catbox.moe/user/api.php"
    files = {'fileToUpload': ('screenshot.png', image_bytes, 'image/png')}
    data = {'reqtype': 'fileupload'}
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error uploading to Catbox: {e}")
    return None

def extract_page_id(url):
    match = re.search(r'([a-f0-9]{32})', url.replace('-', ''))
    if match:
        return match.group(1)
    return url.replace('-', '')

def append_to_notion(token, page_id, image_url, description):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    data = {
        "children": []
    }
    
    if image_url:
        data["children"].append({
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": image_url
                }
            }
        })
        
    if description:
        data["children"].append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": description
                        }
                    }
                ]
            }
        })
        
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text

class SnippingWidget(QWidget):
    on_snip_completed = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: transparent;")
        
        screen = QApplication.primaryScreen()
        self.full_screen_pixmap = screen.grabWindow(0)
        self.setGeometry(0, 0, self.full_screen_pixmap.width(), self.full_screen_pixmap.height())

        self.begin = QPoint()
        self.end = QPoint()
        self.is_snipping = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.full_screen_pixmap)
        
        # Draw dark overlay
        overlay_color = QColor(0, 0, 0, 100) # Semi-transparent black
        painter.fillRect(self.rect(), overlay_color)
        
        if self.is_snipping:
            rect = QRect(self.begin, self.end).normalized()
            # Clear the overlay inside the rect
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, Qt.white)
            
            # Draw the actual image inside the cleared area
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.drawPixmap(rect, self.full_screen_pixmap, rect)
            
            # Draw a border around the selection
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.is_snipping = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_snipping:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_snipping:
            self.is_snipping = False
            rect = QRect(self.begin, self.end).normalized()
            if rect.width() > 0 and rect.height() > 0:
                cropped = self.full_screen_pixmap.copy(rect)
                self.on_snip_completed.emit(cropped)
            else:
                self.show_main_window()
            self.close()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.show_main_window()
            self.close()
            
    def show_main_window(self):
        # We handle this by not emitting the signal, but we still need to show main window.
        # Instead, we emit an empty pixmap to signal cancellation
        self.on_snip_completed.emit(QPixmap())

class DrawingLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.lastPoint = QPoint()
        self.penColor = QColor(255, 0, 0) # Default red
        self.penWidth = 4

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.pixmap())
            pen = QPen(self.penColor, self.penWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot & Note to Notion")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Controls Layout
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)
        
        self.btn_screenshot_full = QPushButton("📸 Full Screenshot")
        self.btn_screenshot_full.setStyleSheet("padding: 10px; background-color: #1976D2; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_screenshot_full.clicked.connect(self.take_full_screenshot)
        self.controls_layout.addWidget(self.btn_screenshot_full)
        
        self.btn_screenshot_custom = QPushButton("✂️ Custom Screenshot")
        self.btn_screenshot_custom.setStyleSheet("padding: 10px; background-color: #9C27B0; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_screenshot_custom.clicked.connect(self.take_custom_screenshot)
        self.controls_layout.addWidget(self.btn_screenshot_custom)
        
        self.btn_color = QPushButton("🎨 Change Pen Color")
        self.btn_color.setStyleSheet("padding: 10px; background-color: #FF9800; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_color.clicked.connect(self.change_color)
        self.controls_layout.addWidget(self.btn_color)
        
        self.btn_clear = QPushButton("🗑️ Clear Drawing")
        self.btn_clear.setStyleSheet("padding: 10px; background-color: #f44336; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_clear.clicked.connect(self.clear_drawing)
        self.controls_layout.addWidget(self.btn_clear)
        
        # Image Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #eeeeee;")
        self.image_label = DrawingLabel()
        self.image_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Default placeholder pixmap
        default_pixmap = QPixmap(800, 400)
        default_pixmap.fill(QColor(230, 230, 230))
        painter = QPainter(default_pixmap)
        painter.setFont(QFont("Arial", 16))
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(default_pixmap.rect(), Qt.AlignCenter, "Click 'Take Screenshot' to start")
        painter.end()
        self.image_label.setPixmap(default_pixmap)
        self.image_label.setFixedSize(default_pixmap.size())
        
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area, stretch=1)
        
        self.original_pixmap = None
        
        # Inputs Layout
        self.inputs_layout = QVBoxLayout()
        self.layout.addLayout(self.inputs_layout)
        
        self.desc_label = QLabel("Description (Catatan / Penjelasan):")
        self.desc_label.setStyleSheet("font-weight: bold;")
        self.inputs_layout.addWidget(self.desc_label)
        self.text_desc = QTextEdit()
        self.text_desc.setMaximumHeight(100)
        self.text_desc.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 5px;")
        self.inputs_layout.addWidget(self.text_desc)
        
        self.notion_layout = QHBoxLayout()
        self.inputs_layout.addLayout(self.notion_layout)
        
        self.notion_layout.addWidget(QLabel("Notion Page Link:"))
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://www.notion.so/...")
        self.input_url.setStyleSheet("background-color: white; padding: 5px;")
        self.notion_layout.addWidget(self.input_url)
        
        self.notion_layout.addWidget(QLabel("Notion Integration Token:"))
        self.input_token = QLineEdit()
        self.input_token.setEchoMode(QLineEdit.Password)
        self.input_token.setPlaceholderText("secret_...")
        self.input_token.setStyleSheet("background-color: white; padding: 5px;")
        self.notion_layout.addWidget(self.input_token)
        
        # Try load from file
        try:
            with open("notion_config.txt", "r") as f:
                lines = f.read().splitlines()
                if len(lines) >= 1: self.input_token.setText(lines[0])
                if len(lines) >= 2: self.input_url.setText(lines[1])
        except:
            pass
            
        self.btn_save = QPushButton("🚀 2. Save to Notion")
        self.btn_save.setMinimumHeight(50)
        self.btn_save.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 16px; border-radius: 5px;")
        self.btn_save.clicked.connect(self.save_to_notion)
        self.layout.addWidget(self.btn_save)

    def take_full_screenshot(self):
        self.hide()
        # Wait a bit for window to hide
        QTimer.singleShot(400, self._capture_full)
        
    def _capture_full(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        self.set_screenshot(screenshot)
        self.show()

    def take_custom_screenshot(self):
        self.hide()
        QTimer.singleShot(400, self._start_snipping)
        
    def _start_snipping(self):
        self.snipper = SnippingWidget()
        self.snipper.on_snip_completed.connect(self._capture_custom)
        self.snipper.show()
        
    def _capture_custom(self, pixmap):
        if not pixmap.isNull():
            self.set_screenshot(pixmap)
        self.show()
        
    def set_screenshot(self, pixmap):
        self.original_pixmap = pixmap.copy()
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())

    def change_color(self):
        color = QColorDialog.getColor(self.image_label.penColor, self)
        if color.isValid():
            self.image_label.penColor = color

    def clear_drawing(self):
        if self.original_pixmap:
            self.image_label.setPixmap(self.original_pixmap.copy())

    def save_to_notion(self):
        if not self.original_pixmap:
            QMessageBox.warning(self, "Error", "Silakan ambil screenshot terlebih dahulu!")
            return
            
        token = self.input_token.text().strip()
        url = self.input_url.text().strip()
        desc = self.text_desc.toPlainText()
        
        if not token or not url:
            QMessageBox.warning(self, "Error", "Silakan masukkan Token Notion dan Link Page Notion.")
            return
            
        # Save config
        with open("notion_config.txt", "w") as f:
            f.write(f"{token}\n{url}")
            
        self.btn_save.setEnabled(False)
        self.btn_save.setText("⏳ Mengunggah Gambar...")
        QApplication.processEvents()
        
        # Get image bytes
        pixmap = self.image_label.pixmap()
        byte_array = QBuffer()
        byte_array.open(QIODevice.ReadWrite)
        pixmap.save(byte_array, "PNG")
        image_bytes = byte_array.data().data()
        
        # Upload to Catbox
        image_url = upload_to_catbox(image_bytes)
        
        if not image_url:
            QMessageBox.critical(self, "Error", "Gagal mengunggah gambar ke internet.")
            self.btn_save.setEnabled(True)
            self.btn_save.setText("🚀 2. Save to Notion")
            return
            
        self.btn_save.setText("⏳ Mengirim ke Notion...")
        QApplication.processEvents()
        
        page_id = extract_page_id(url)
        success, response = append_to_notion(token, page_id, image_url, desc)
        
        self.btn_save.setEnabled(True)
        self.btn_save.setText("🚀 2. Save to Notion")
        
        if success:
            QMessageBox.information(self, "Berhasil!", "Screenshot dan catatan berhasil ditambahkan ke Notion!")
            self.text_desc.clear()
        else:
            QMessageBox.critical(self, "Error", f"Gagal menambahkan ke Notion:\n{response}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
