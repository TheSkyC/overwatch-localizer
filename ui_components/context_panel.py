# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QSizePolicy
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor  # 确保 QTextCursor 已导入
from PySide6.QtCore import Qt
from utils.localization import _


class ContextPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("yellow"))
        self.highlight_format.setForeground(QColor("black"))  # 确保高亮背景下的文字清晰

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.context_text_display = QTextEdit()
        self.context_text_display.setReadOnly(True)
        self.context_text_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.context_text_display.setFontFamily("Consolas")
        self.context_text_display.setFontPointSize(9)
        self.context_text_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.context_text_display)

    def set_context(self, context_lines, current_line_in_context_idx):
        self.context_text_display.clear()

        if not context_lines:
            self.context_text_display.setPlainText("")
            return

        processed_lines = [line.replace('\t', '    ') for line in context_lines]
        full_text = "\n".join(processed_lines)
        self.context_text_display.setPlainText(full_text)

        if 0 <= current_line_in_context_idx < len(context_lines):
            doc = self.context_text_display.document()
            current_block = doc.findBlockByNumber(current_line_in_context_idx)

            if not current_block.isValid():
                return
            block_format = current_block.blockFormat()
            block_format.setBackground(self.highlight_format.background())  # 只设置背景色
            cursor = QTextCursor(current_block)
            cursor.setBlockFormat(block_format)
            scroll_target_cursor = QTextCursor(doc)
            scroll_target_cursor.setPosition(current_block.position())
            self.context_text_display.setTextCursor(scroll_target_cursor)
            self.context_text_display.ensureCursorVisible()

    def update_ui_texts(self):
        label = self.findChild(QLabel, "context_label")
