// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO member details", {
    async refresh(frm) {
        await hide_advance_search(frm, ['state_name', 'block_name', 'district_name', 'fpo', 'grampanchayat_name', 'village_name', 'producer_group', 'tribe', 'category'])
        await extend_options_length(frm, ['fpo_name', 'fpo_name', 'district_name', 'fpo', 'producer_group', 'tribe', 'category'])
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('fpo', 'block', frm, frm.doc.block_name)
        await apply_filter('grampanchayat_name', 'block', frm, frm.doc.block_name)
    },
    validate(frm) {
        integer_length_validator(frm.doc.aadhar_number, 12, 'Aadhar Card');
        integer_length_validator(frm.doc.register_aadhar_mobile_number, 10, 'Register Aadhar Mobile Number');
        if (frm.doc.total_own_land < frm.doc.total_own_irrigated_land) {
            frappe.throw(`Total own irrigated land can't be more than Total own land`)
        }
    },
    state_name: async function (frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'fpo', 'grampanchayat_name', 'village_name'])
    },
    district_name: async function (frm) {
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'fpo', 'grampanchayat_name', 'village_name'])
    },
    block_name: async function (frm) {
        await apply_filter('fpo', 'block', frm, frm.doc.block_name)
        await apply_filter('grampanchayat_name', 'block', frm, frm.doc.block_name)
        truncate_multiple_fields_value(frm, ['fpo', 'grampanchayat_name', 'village_name'])
    },
    fpo: async function (frm) {
        await apply_filter('producer_group', 'fpo', frm, frm.doc.fpo)
        truncate_multiple_fields_value(frm, ['producer_group'])
    },
    grampanchayat_name: async function (frm) {
        await apply_filter('village_name', 'grampanchayat', frm, frm.doc.grampanchayat_name)
        truncate_multiple_fields_value(frm, ['village_name'])
    },
    before_save: function (frm) {
        if (frm.doc.mobile_number === '+91-') {
            frm.doc.mobile_number = '';
        }
    },
    aadhar_number(frm) {
        integer_length_validator(frm.doc.aadhar_number, 12, 'Aadhar Card');
    },
    register_aadhar_mobile_number(frm) {
        integer_length_validator(frm.doc.register_aadhar_mobile_number, 10, 'Register Aadhar Mobile Number');
    },
    total_own_irrigated_land(frm) {
        if (frm.doc.total_own_land < frm.doc.total_own_irrigated_land) {
            frappe.throw(`Total own irrigated land can't be more than Total own land`)
        }
    }
});
