// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("District", {
    refresh(frm) {
        hide_advance_search(frm, ['state'])
        extend_options_length(frm, ['state'])
        hide_print_button(frm)
    },
});
