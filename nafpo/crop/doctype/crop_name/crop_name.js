// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crop Name", {
    refresh(frm) {
        hide_advance_search(frm, ['state_name', 'name_of_fpo', 'type_of_crop'])
        extend_options_length(frm, ['state_name', 'name_of_fpo', 'type_of_crop'])
        apply_filter('name_of_fpo', 'state', frm, frm.doc.state_name)
        apply_filter('type_of_crop', 'fpo', frm, frm.doc.name_of_fpo)
    },
    state_name: function (frm) {
        apply_filter('name_of_fpo', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['name_of_fpo', 'type_of_crop'])
    },
    name_of_fpo: function (frm) {
        apply_filter('type_of_crop', 'fpo', frm, frm.doc.name_of_fpo)
        truncate_multiple_fields_value(frm, ['type_of_crop'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    }
});
