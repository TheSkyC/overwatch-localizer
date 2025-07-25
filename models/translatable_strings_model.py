# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel, Signal, QObject
from PySide6.QtGui import QColor, QFont
from difflib import SequenceMatcher
import re
from utils.localization import _
from services.validation_service import placeholder_regex

NewlineColorRole = Qt.UserRole + 1

class TranslatableStringsModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self._id_to_index_map = {obj.id: i for i, obj in enumerate(self._data)}
        self.headers = ["#", "S", "Original", "Translation", "Comment", "✔", "Line"]
        self.app_instance = parent

    def set_translatable_objects(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self._id_to_index_map = {obj.id: i for i, obj in enumerate(self._data)}
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        row, col = index.row(), index.column()
        if row >= len(self._data): return None
        ts_obj = self._data[row]
        original_display_text = None
        if role == Qt.DisplayRole:
            if col == 2:
                original_display_text = ts_obj.original_semantic
            elif col == 3:
                original_display_text = ts_obj.get_translation_for_ui()

            if original_display_text is not None:
                column_name = 'original' if col == 2 else 'translation'
                display_text = self.app_instance.plugin_manager.run_hook(
                    'process_string_for_display',
                    original_display_text,
                    ts_object=ts_obj,
                    column=column_name
                )
        if role == Qt.BackgroundRole:
            return ts_obj.ui_style_cache.get('background')

        if role == Qt.ForegroundRole:
            return ts_obj.ui_style_cache.get('foreground')

        if role == Qt.FontRole:
            return ts_obj.ui_style_cache.get('font')

        if role == NewlineColorRole:
            if col in [2, 3]:
                return ts_obj.ui_style_cache.get('newline_color')
            return None

        if role == Qt.DisplayRole:
            if col == 0:
                return row + 1
            elif col == 1:
                if ts_obj.warnings and not ts_obj.is_warning_ignored:
                    return "⚠️"
                elif ts_obj.is_ignored:
                    return "I"
                elif ts_obj.translation.strip():
                    if ts_obj.minor_warnings and not ts_obj.is_warning_ignored:
                        return "*T"
                    return "T"
                else:
                    return "U"
            elif col == 2:
                return display_text
            elif col == 3:
                return display_text
            elif col == 4:
                return ts_obj.comment
            elif col == 5:
                return "✔" if ts_obj.is_reviewed else ""
            elif col == 6:
                return ts_obj.line_num_in_file

        if role == Qt.UserRole:
            return ts_obj

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section < len(self.headers):
                header_text = self.headers[section]
                try:
                    return _(header_text)
                except:
                    return header_text
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index_from_id(self, ts_id):
        if ts_id in self._id_to_index_map:
            row = self._id_to_index_map[ts_id]
            return self.index(row, 0)
        return QModelIndex()


class TranslatableStringsProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_ignored = True
        self.show_untranslated = False
        self.show_translated = False
        self.show_unreviewed = False
        self.search_term = ""
        self.search_results_indices = set()
        self.is_po_mode = False
        self._current_filter_seen_originals = set()
        self.new_entry_id = "##NEW_ENTRY##"
        self.setDynamicSortFilter(True)

    def set_filters(self, show_ignored, show_untranslated, show_translated, show_unreviewed, search_term, is_po_mode):
        current_sort_column = self.sortColumn()
        current_sort_order = self.sortOrder()
        self.show_ignored = show_ignored
        self.show_untranslated = show_untranslated
        self.show_translated = show_translated
        self.show_unreviewed = show_unreviewed
        self.search_term = search_term.lower()
        self.is_po_mode = is_po_mode
        self.invalidateFilter()
        self.sort(current_sort_column, current_sort_order)

    def filterAcceptsRow(self, source_row, source_parent):
        ts_obj = self.sourceModel().data(self.sourceModel().index(source_row, 0, source_parent), Qt.UserRole)
        if not ts_obj:
            return False
        if self.is_po_mode and ts_obj.id == self.new_entry_id:
            return True
        if self.search_term:
            if not (self.search_term in ts_obj.original_semantic.lower() or
                    self.search_term in ts_obj.get_translation_for_ui().lower() or
                    self.search_term in ts_obj.comment.lower()):
                return False
        has_translation = bool(ts_obj.translation.strip())
        if not self.show_ignored and ts_obj.is_ignored: return False
        if self.show_untranslated and has_translation and not ts_obj.is_ignored: return False
        if self.show_translated and not has_translation and not ts_obj.is_ignored: return False
        if self.show_unreviewed and ts_obj.is_reviewed: return False

        return True

    def lessThan(self, left_index, right_index):
        left_obj = self.sourceModel().data(left_index, Qt.UserRole)
        right_obj = self.sourceModel().data(right_index, Qt.UserRole)

        if not left_obj or not right_obj:
            return False
        if self.is_po_mode:
            if left_obj.id == self.new_entry_id: return False
            if right_obj.id == self.new_entry_id: return True
        column = self.sortColumn()
        if column == 0:
            return left_index.row() < right_index.row()
        elif column == 1 or column == 5:
            def get_status_weight(ts_obj):
                if ts_obj.is_ignored: return 5
                if ts_obj.is_reviewed: return 4
                if ts_obj.warnings and not ts_obj.is_warning_ignored: return 0
                if not ts_obj.translation.strip(): return 1
                if ts_obj.minor_warnings and not ts_obj.is_warning_ignored: return 2
                return 3
            left_weight = get_status_weight(left_obj)
            right_weight = get_status_weight(right_obj)
            if left_weight != right_weight:
                return left_weight < right_weight
            else:
                return left_obj.line_num_in_file < right_obj.line_num_in_file
        elif column == 2:
            return left_obj.original_semantic.lower() < right_obj.original_semantic.lower()
        elif column == 3:
            return left_obj.get_translation_for_ui().lower() < right_obj.get_translation_for_ui().lower()
        elif column == 4:
            return left_obj.comment.lower() < right_obj.comment.lower()
        elif column == 6:
            return left_obj.line_num_in_file < right_obj.line_num_in_file

        return False

    def invalidateFilter(self):
        self._current_filter_seen_originals.clear()
        super().invalidateFilter()

    def id_in_filtered_data(self, ts_id):
        source_index = self.sourceModel().index_from_id(ts_id)
        if source_index.isValid():
            proxy_index = self.mapFromSource(source_index)
            return proxy_index.isValid()
        return False

    def set_static_sorting_enabled(self, enabled: bool):
        self.setDynamicSortFilter(not enabled)