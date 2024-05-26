// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crop POP", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'district', 'block', 'fpo', 'crop_type', 'crop_name'])
        extend_options_length(frm, ['state', 'district', 'block', 'fpo', 'crop_type', 'crop_name'])
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        apply_filter('fpo', 'block', frm, frm.doc.block)
        apply_filter('crop_type', 'fpo', frm, frm.doc.fpo)
        apply_filter('crop_name', 'type_of_crop', frm, frm.doc.crop_type)
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block', 'fpo', 'crop_type', 'crop_name'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block', 'fpo', 'crop_type', 'crop_name'])
    },
    block: function (frm) {
        apply_filter('fpo', 'block', frm, frm.doc.block)
        truncate_multiple_fields_value(frm, ['fpo', 'crop_type', 'crop_name'])
    },
    fpo: function (frm) {
        apply_filter('crop_type', 'fpo', frm, frm.doc.fpo)
        truncate_multiple_fields_value(frm, ['crop_type', 'crop_name'])
    },
    crop_type: function (frm) {
        apply_filter('crop_name', 'type_of_crop', frm, frm.doc.crop_type)
        truncate_multiple_fields_value(frm, ['crop_name'])
    }
});
