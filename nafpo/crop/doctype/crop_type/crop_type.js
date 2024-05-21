// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crop Type", {
    refresh(frm) {
        hide_advance_search(frm, ['state_name', 'fpo'])
        extend_options_length(frm, ['state_name', 'fpo'])
        apply_filter('fpo', 'state', frm, frm.doc.state_name)
    },
    state_name: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo'])
    }
});
