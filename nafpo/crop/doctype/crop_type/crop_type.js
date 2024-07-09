// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
let new_entry = false;
frappe.ui.form.on("Crop Type", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'fpo', 'single_state', 'single_fpo'])
        extend_options_length(frm, ['state', 'fpo', 'single_state', 'single_fpo'])
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
    },
    before_save: function (frm) {
        if (frm.doc.__islocal) {
            new_entry = true;
        } else {
            new_entry = false;
        }
    },
    after_save: function () {
        if (new_entry) {
            change_route();
        }
    },
    state: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    single_state: function (frm) {
        apply_filter('single_fpo', 'state', frm, frm.doc.single_state)
        truncate_multiple_fields_value(frm, ['single_fpo'])
    },
});

var change_route = function () {
    frappe.set_route("List", "Crop Type");
}
