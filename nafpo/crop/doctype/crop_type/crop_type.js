// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crop Type", {
    refresh(frm) {
        // if (frm.is_new()) {
        //     frm.set_df_property('state', 'read_only', 1); state
        // }
        hide_advance_search(frm, ['state', 'fpo'])
        extend_options_length(frm, ['state', 'fpo'])
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
    },
    after_save: function (frm) {
        change_route(frm);
    },
    state: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    }
});

var change_route = function (frm) {
    frappe.set_route("List", "Crop Type");
}
