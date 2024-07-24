// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Producer Groups", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'fpo'])
        extend_options_length(frm, ['state', 'fpo'])
        apply_filter('fpo', 'state', frm, frm.doc.state)
    },
    onload(frm) {
    },
    validate(frm) {
        validate_string(frm, 'contact_number', "Contact Number");
    },
    state: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    contact_number(frm) {
        validate_string(frm, 'contact_number', "Contact Number");
    }
});
