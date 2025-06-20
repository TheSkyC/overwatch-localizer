# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

import tkinter as tk
from tkinter import ttk, simpledialog
from utils.localization import _

class DiffDialog(simpledialog.Dialog):
    def __init__(self, parent, title, diff_results):
        self.diff_results = diff_results

        self.parent = parent
        self.result = None

        tk.Toplevel.__init__(self, parent)
        self.withdraw()

        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            super().title(title)

        main_container = ttk.Frame(self)
        self.initial_focus = self.body(main_container)
        main_container.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        main_container.grid_rowconfigure(0, weight=0)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        self.buttonbox(main_container)

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry(f"1200x700+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")

        self.deiconify()
        self.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def body(self, master):
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)

        summary_text = self.diff_results.get('summary', _('Comparison Results Summary'))
        summary_label = ttk.Label(
            master,
            text=summary_text,
            wraplength=1100,
            justify=tk.LEFT,
            font=('Segoe UI', 10, 'bold')
        )
        summary_label.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 10))

        tree_container = ttk.Frame(master)
        tree_container.grid(row=1, column=0, sticky="nsew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        cols = ("status", "old_text", "new_text", "similarity")

        self.tree = ttk.Treeview(tree_container, columns=cols, show="headings")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.heading("status", text=_("Status"))
        self.tree.heading("old_text", text=_("Old Version Original"))
        self.tree.heading("new_text", text=_("New Version Original"))
        self.tree.heading("similarity", text=_("Similarity"))

        self.tree.column("status", width=80, anchor=tk.W)
        self.tree.column("old_text", width=500, anchor=tk.W)
        self.tree.column("new_text", width=500, anchor=tk.W)
        self.tree.column("similarity", width=80, anchor=tk.CENTER)

        self.tree.tag_configure('added', background='#DFF0D8', foreground='#3C763D')
        self.tree.tag_configure('removed', background='#F2DEDE', foreground='#A94442')
        self.tree.tag_configure('modified', background='#FCF8E3', foreground='#8A6D3B')

        self.populate_tree()

        return self.tree

    def buttonbox(self, master):
        box = ttk.Frame(master)
        ttk.Button(box, text=_("Confirm and Update Project"), width=18, command=self.ok, default=tk.ACTIVE).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Button(box, text=_("Cancel"), width=10, command=self.cancel).pack(
            side=tk.LEFT, padx=5, pady=5)
        box.grid(row=2, column=0, sticky="e", pady=(5, 0))

        self.bind("<Escape>", self.cancel)
        self.bind("<Return>", self.ok)

    def populate_tree(self):
        for item in self.diff_results['added']:
            self.tree.insert("", "end",
                             values=(_("Added"), "", item['new_obj'].original_semantic, "N/A"),
                             tags=('added',))

        for item in self.diff_results['removed']:
            self.tree.insert("", "end",
                             values=(_("Removed"), item['old_obj'].original_semantic, "", "N/A"),
                             tags=('removed',))

        for item in self.diff_results['modified']:
            sim_str = f"{item['similarity']:.2%}"
            self.tree.insert("", "end",
                             values=(_("Modified/Inherited"), item['old_obj'].original_semantic,
                                     item['new_obj'].original_semantic, sim_str),
                             tags=('modified',))

    def apply(self):
        self.result = True