// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO member details", {
    async refresh(frm) {
        hide_advance_search(frm, ['state_name', 'block_name', 'district_name', 'fpo', 'grampanchayat_name', 'village_name', 'producer_group', , 'category'])
        extend_options_length(frm, ['fpo_name', 'fpo_name', 'district_name', 'fpo', 'producer_group', 'tribe', 'category'])
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('fpo', 'district', frm, frm.doc.district_name)
        await apply_filter('grampanchayat_name', 'block', frm, frm.doc.block_name)
        await apply_filter('producer_group', 'fpo', frm, frm.doc.fpo)
    },
    validate(frm) {
        validate_string(frm, 'aadhar_number', "Aadhar Number");
        validate_string(frm, 'register_aadhar_mobile_number', "Register Aadhar Mobile Number");
        validate_string(frm, 'bank_ac_number', "Bank Account Number");
        validate_string(frm, 'mobile_number', "Mobile Number");
        if (frm.doc.total_own_land < frm.doc.total_own_irrigated_land) {
            frappe.throw({ message: `Total own land must be greater than or equal to "Total own irrigated land".` })
        }
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
    },
    state_name: async function (frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'fpo', 'grampanchayat_name', 'village_name'])
    },
    district_name: async function (frm) {
        await apply_filter('fpo', 'district', frm, frm.doc.district_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'fpo', 'grampanchayat_name', 'village_name'])
    },
    bank_ac_number(frm) {
        validate_string(frm, 'bank_ac_number', "Bank Account Number");
    },
    block_name: async function (frm) {
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
    // before_save: function (frm) {
    //     if (frm.doc.mobile_number === '+91-') {
    //         frm.doc.mobile_number = '';
    //     }
    // },
    aadhar_number(frm) {
        validate_string(frm, 'aadhar_number', "Aadhar Number");
    },
    register_aadhar_mobile_number(frm) {
        validate_string(frm, 'register_aadhar_mobile_number', "Register Aadhar Mobile Number");
    },
    mobile_number(frm) {
        validate_string(frm, 'mobile_number', "Mobile Number");
    },
    total_own_land: async function (frm) {
        await frm.set_value('total_owned_in_hectare', frm.doc.total_own_land * 0.404686)
    },
    total_own_irrigated_land: async function (frm) {
        if (frm.doc.total_own_land < frm.doc.total_own_irrigated_land) {
            frappe.throw({ message: `Total own land must be greater than or equal to "Total own irrigated land".` })
        }
        await frm.set_value('total_own_irrigated_land_in_hectare', frm.doc.total_own_irrigated_land * 0.404686)
    },
    do_you_have_any_leased_land_area_in_acre(frm) {
        if (frm.doc.do_you_have_any_leased_land_area_in_acre == "No") {
            frm.set_value('how_much_irrigated_leased_land_area_in_acre', 0)
            frm.set_value('how_much_irrigated_leased_land_in_hectare', 0)
        }
    },
    how_much_irrigated_leased_land_area_in_acre: async function (frm) {
        if (frm.doc.do_you_have_any_leased_land_area_in_acre == "Yes") {
            await frm.set_value('how_much_irrigated_leased_land_in_hectare', frm.doc.how_much_irrigated_leased_land_area_in_acre * 0.404686)
        }
    },
    consent_image(frm) {
        frm.image_uploaded = true;
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
});
