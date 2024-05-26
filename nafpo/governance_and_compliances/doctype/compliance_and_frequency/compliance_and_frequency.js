// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Compliance and Frequency", {
    refresh(frm) {
        hide_advance_search(frm, ['compliance', 'frequency', 'state_name', 'district_name', 'block_name', 'fpo_name', 'member'])
        extend_options_length(frm, ['compliance', 'frequency', 'state_name', 'district_name', 'block_name', 'fpo_name', 'member'])
        apply_filter('district_name', 'state', frm, frm.doc.state_name)
        apply_filter('block_name', 'district', frm, frm.doc.district_name)
        apply_filter('fpo_name', 'block', frm, frm.doc.block_name)
        apply_filter('member', 'fpo', frm, frm.doc.fpo_name)
    },
    state_name: function (frm) {
        apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'fpo_name', 'member'])
    },
    district_name: function (frm) {
        apply_filter('block_name', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'fpo_name', 'member'])
    },
    block_name: function (frm) {
        apply_filter('fpo_name', 'block', frm, frm.doc.block_name)
        truncate_multiple_fields_value(frm, ['fpo_name', 'member'])
    },
    fpo_name: function (frm) {
        apply_filter('member', 'fpo', frm, frm.doc.fpo_name)
        truncate_multiple_fields_value(frm, ['member'])
    },
});
