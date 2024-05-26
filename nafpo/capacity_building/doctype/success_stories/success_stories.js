// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Success Stories", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'district', 'block', 'fpo', 'category', 'language_of_training_material', 'language_of_module'])
        extend_options_length(frm, ['state', 'district', 'block', 'fpo', 'category', 'language_of_training_material', 'language_of_module'])
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        apply_filter('fpo', 'block', frm, frm.doc.block)
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block', 'fpo'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block', 'fpo'])
    },
    block: function (frm) {
        apply_filter('fpo', 'block', frm, frm.doc.block)
        truncate_multiple_fields_value(frm, ['fpo'])
    }
});
