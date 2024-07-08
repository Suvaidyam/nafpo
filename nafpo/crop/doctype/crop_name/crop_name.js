// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

let new_entry = false;
frappe.ui.form.on("Crop Name", {
    refresh(frm) {
        hide_advance_search(frm, ['state_name', 'fpo', 'type_of_crop'])
        extend_options_length(frm, ['state_name', 'fpo', 'type_of_crop'])
        apply_filter('fpo', 'state', frm, frm.doc.state_name)
        apply_filter('type_of_crop', 'single_fpo', frm, frm.doc.fpo)
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
    state_name: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo', 'type_of_crop'])
    },
    fpo: function (frm) {
        apply_filter('type_of_crop', 'single_fpo', frm, frm.doc.fpo)
        truncate_multiple_fields_value(frm, ['type_of_crop'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    }
});

var change_route = function () {
    frappe.set_route("List", "Crop Name");
}
