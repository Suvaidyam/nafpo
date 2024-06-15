// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("District", {
    refresh(frm) {
        hide_advance_search(frm, ['state'])
        extend_options_length(frm, ['state'])
        frm.is_new() ? hide_print_button(frm) : show_print_button(frm);
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
});
