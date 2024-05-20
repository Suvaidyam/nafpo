// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Block", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'district'])
        extend_options_length(frm, ['state', 'district'])
        apply_filter('district', 'state', frm, frm.doc.state)
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district'])
    }
});
