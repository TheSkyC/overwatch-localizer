# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeySequence, QAction
from utils.constants import DEFAULT_KEYBINDINGS
from utils.localization import _

class KeybindingDialog(QDialog):
    def __init__(self, parent, title, app_instance):
        super().__init__(parent)
        self.app = app_instance
        self.key_vars = {}
        self.current_capture_entry = None

        self.ACTION_MAP = {
            'open_code_file': self.app.action_open_code_file,
            'open_project': self.app.action_open_project,
            'save_current_file': self.app.action_save_current_file,
            'save_code_file': self.app.action_save_code_file,
            'undo': self.app.action_undo,
            'redo': self.app.action_redo,
            'find_replace': self.app.action_find_replace,
            'copy_original': self.app.action_copy_original,
            'paste_translation': self.app.action_paste_translation,
            'ai_translate_selected': self.app.action_ai_translate_selected,
            'toggle_reviewed': {'text': _("Toggle Reviewed Status")},
            'toggle_ignored': {'text': _("Toggle Ignored Status")},
            'apply_and_next': {'text': _("Apply and Go to Next Untranslated")},
        }

        self.pressed_modifiers = set()
        self.modifier_map = {
            Qt.Key_Control: 'Control', Qt.Key_Shift: 'Shift',
            Qt.Key_Alt: 'Alt', Qt.Key_Meta: 'Meta'
        }
        self.modifier_names = {
            Qt.ControlModifier: 'Control',
            Qt.ShiftModifier: 'Shift',
            Qt.AltModifier: 'Alt',
            Qt.MetaModifier: 'Meta'
        }

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 600)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QVBoxLayout()

        self.entries = {}
        for action_name, action_obj in self.ACTION_MAP.items():
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            description = action_obj.text().replace('&', '') if isinstance(action_obj, QAction) else action_obj['text']
            row_layout.addWidget(QLabel(description + ":"))

            key_sequence_str = self.app.config['keybindings'].get(action_name, DEFAULT_KEYBINDINGS.get(action_name, ''))
            entry = QLineEdit(key_sequence_str)
            entry.setReadOnly(True)
            entry.mousePressEvent = lambda event, e=entry: self.on_entry_click(e, event)
            row_layout.addWidget(entry)

            form_layout.addWidget(row_widget)

            self.key_vars[action_name] = entry
            self.entries[action_name] = entry

        main_layout.addLayout(form_layout)
        main_layout.addStretch(1)

        button_box = QHBoxLayout()
        reset_btn = QPushButton(_("Reset to Defaults"))
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_box.addWidget(reset_btn)
        button_box.addStretch(1)

        ok_btn = QPushButton(_("OK"))
        ok_btn.clicked.connect(self.accept)
        button_box.addWidget(ok_btn)

        cancel_btn = QPushButton(_("Cancel"))
        cancel_btn.clicked.connect(self.reject)
        button_box.addWidget(cancel_btn)
        main_layout.addLayout(button_box)

    def on_entry_click(self, entry, event):
        if event.button() == Qt.LeftButton:
            self.current_capture_entry = entry
            self.current_capture_entry.setStyleSheet("background-color: lightblue;")
            self.current_capture_entry.setText(_("Press a key combination..."))
            self.pressed_modifiers.clear()
            self.installEventFilter(self)
        QLineEdit.mousePressEvent(entry, event)

    def eventFilter(self, obj, event):
        if self.current_capture_entry and event.type() == QEvent.KeyPress:
            key_event = event
            key = key_event.key()
            modifiers = key_event.modifiers()
            if key in [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta]:
                return True

            parts = []
            if modifiers & Qt.ControlModifier: parts.append('Control')
            if modifiers & Qt.ShiftModifier: parts.append('Shift')
            if modifiers & Qt.AltModifier: parts.append('Alt')
            if modifiers & Qt.MetaModifier: parts.append('Meta')

            key_name = QKeySequence(key).toString(QKeySequence.NativeText)
            if key_name and key_name not in parts:
                parts.append(key_name)

            key_sequence_str = "+".join(parts)
            self.current_capture_entry.setText(key_sequence_str)
            for action_name, entry_widget in self.entries.items():
                if entry_widget == self.current_capture_entry:
                    self.key_vars[action_name].setText(key_sequence_str)
                    break

            self.stop_capture()
            return True
        return super().eventFilter(obj, event)

    def stop_capture(self):
        if self.current_capture_entry:
            self.current_capture_entry.setStyleSheet("")
            self.current_capture_entry = None
        self.removeEventFilter(self)

    def reset_to_defaults(self):
        reply = QMessageBox.question(self, _("Confirm"), _("Are you sure you want to reset all keybindings to their default settings?"),
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for action_name, key_sequence in DEFAULT_KEYBINDINGS.items():
                if action_name in self.key_vars:
                    self.key_vars[action_name].setText(key_sequence)

    def accept(self):
        self.stop_capture()
        new_bindings = {}
        for action_name, entry_widget in self.key_vars.items():
            new_bindings[action_name] = entry_widget.text().strip()
        self.app.config['keybindings'] = new_bindings
        self.app.save_config()
        self.app.update_statusbar(_("Keybindings have been updated."))
        super().accept()

    def reject(self):
        self.stop_capture()
        super().reject()
