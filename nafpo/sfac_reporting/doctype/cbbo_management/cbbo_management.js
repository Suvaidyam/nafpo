// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("CBBO Management", {
    refresh(frm) {
        hide_advance_search(frm, ['select_fpo'])
        extend_options_length(frm, ['select_fpo'])
    },
});
