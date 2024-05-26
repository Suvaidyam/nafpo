// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Email Directory", {
    refresh(frm) {
        hide_advance_search(frm, ['fpo_name'])
        extend_options_length(frm, ['fpo_name'])
    }
});
