// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO Profiling", {
    async refresh(frm) {
        hide_advance_search(frm, ['bod_kyc_name', 'name_of_cbbo', 'state_name',
            'block_name', 'district_name', 'name_of_the_fpo'
        ])
        extend_options_length(frm, ['fpo_name', 'fpo_name', 'district_name', 'name_of_the_fpo', 'bod_kyc_name', 'name_of_cbbo'])
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('name_of_the_fpo', 'block', frm, frm.doc.block_name, true)
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
    },
    state_name: async function (frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'name_of_the_fpo', 'bod_kyc_name'])
    },
    district_name: async function (frm) {
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'name_of_the_fpo'])
    },
    block_name: async function (frm) {
        await apply_filter('name_of_the_fpo', 'block', frm, frm.doc.block_name, true)
        truncate_multiple_fields_value(frm, ['name_of_the_fpo'])
    },
    name_of_the_fpo: async function (frm) {
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        truncate_multiple_fields_value(frm, ['bod_kyc_name', 'fpos_address', 'fpos_pincode'])
    }
});
