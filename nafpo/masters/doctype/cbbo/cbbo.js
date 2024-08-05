// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("CBBO", {
    refresh(frm) {
        frm.is_new() ? hide_print_button(frm) : show_print_button(frm);
        hide_advance_search(frm, ['ia_name'])
        extend_options_length(frm, ['ia_name'])
    },
});
