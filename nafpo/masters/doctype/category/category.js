// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Category", {
    refresh(frm) {
        frm.is_new() ? hide_print_button(frm) : show_print_button(frm);
    },
});
