// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Village", {
    refresh(frm) {
        frm.is_new() ? hide_print_button(frm) : show_print_button(frm);
        hide_advance_search(frm, ['state', 'district', 'block', 'grampanchayat'])
        extend_options_length(frm, ['state', 'district', 'block', 'grampanchayat'])
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        apply_filter('grampanchayat', 'block', frm, frm.doc.block)
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block', 'grampanchayat'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block', 'grampanchayat'])
    },
    block: function (frm) {
        apply_filter('grampanchayat', 'block', frm, frm.doc.block)
        truncate_multiple_fields_value(frm, ['grampanchayat'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
});