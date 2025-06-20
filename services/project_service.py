# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

import json
import os
from tkinter import messagebox
from models.translatable_string import TranslatableString
from utils.constants import APP_VERSION

def load_project(project_filepath):
    with open(project_filepath, 'r', encoding='utf-8') as f:
        project_data = json.load(f)

    if not all(k in project_data for k in ["version", "original_code_file_path", "translatable_objects_data"]):
        raise ValueError("项目文件格式不正确或缺少必要字段。")

    original_code_file_path = project_data["original_code_file_path"]
    original_raw_code_content = ""
    full_code_lines_for_project = []

    if original_code_file_path and os.path.exists(original_code_file_path):
        try:
            with open(original_code_file_path, 'r', encoding='utf-8', errors='replace') as cf:
                original_raw_code_content = cf.read()
            full_code_lines_for_project = original_raw_code_content.splitlines()
        except Exception as e_code:
            messagebox.showwarning("项目警告",
                                   f"无法加载项目关联的代码文件 '{original_code_file_path}': {e_code}\n上下文预览可能不可用。")
    elif original_code_file_path:
        messagebox.showwarning("项目警告",
                               f"项目关联的代码文件 '{original_code_file_path}' 未找到。\n上下文预览和保存到代码文件功能将受限。")

    translatable_objects = [
        TranslatableString.from_dict(ts_data, full_code_lines_for_project)
        for ts_data in project_data["translatable_objects_data"]
    ]

    return {
        "project_data": project_data,
        "original_code_file_path": original_code_file_path,
        "original_raw_code_content": original_raw_code_content,
        "translatable_objects": translatable_objects
    }

def save_project(filepath, app_instance):
    if not app_instance.current_code_file_path and not app_instance.translatable_objects and not app_instance.original_raw_code_content:
        messagebox.showerror("保存项目错误", "无法保存项目：没有关联的代码文件、PO源或可翻译内容。", parent=app_instance.root)
        return False

    project_data = {
        "version": APP_VERSION,
        "original_code_file_path": app_instance.current_code_file_path or "",
        # original_raw_code_content is not saved in project file, it's reloaded from original_code_file_path
        "translatable_objects_data": [ts.to_dict() for ts in app_instance.translatable_objects],
        "project_custom_instructions": app_instance.project_custom_instructions,
        "current_tm_file_path": app_instance.current_tm_file or "",
        "filter_settings": {
            "deduplicate": app_instance.deduplicate_strings_var.get(),
            "show_ignored": app_instance.show_ignored_var.get(),
            "show_untranslated": app_instance.show_untranslated_var.get(),
            "show_translated": app_instance.show_translated_var.get(),
            "show_unreviewed": app_instance.show_unreviewed_var.get(),
        },
        "ui_state": {
            "search_term": app_instance.search_var.get() if app_instance.search_var.get() != "快速搜索..." else "",
            "selected_ts_id": app_instance.current_selected_ts_id or ""
        },
    }
    # Add PO metadata if it exists (from a loaded PO file)
    if app_instance.current_po_metadata:
        project_data["po_metadata"] = app_instance.current_po_metadata


    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("保存项目错误", f"无法保存项目文件: {e}", parent=app_instance.root)
        return False