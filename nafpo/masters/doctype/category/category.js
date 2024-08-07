// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Category", {
    refresh(frm) {
        hide_print_button(frm)
    },
});
