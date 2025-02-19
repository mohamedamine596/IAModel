import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Uploader")
        layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.clicked.connect(self.browse_file)
        layout.addWidget(self.upload_button)

        self.output_label = QLabel("No file uploaded yet.")
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a PDF", "", "PDF Files (*.pdf)")
        if file_path:
            # Replace this with PDF processing
            description = f"Description for {file_path}"
            self.output_label.setText(description)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())