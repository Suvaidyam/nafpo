// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO", {
    refresh(frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        frm.is_new() ? hide_print_button(frm) : show_print_button(frm);
        hide_advance_search(frm, ['state', 'district', 'block', 'cbbo_name'])
        extend_options_length(frm, ['state', 'district', 'block', 'cbbo_name'])
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block'])
    },
});
