// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("CBBO", {
    refresh(frm) {
        hide_advance_search(frm, ['ia_name'])
        extend_options_length(frm, ['ia_name'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
});
