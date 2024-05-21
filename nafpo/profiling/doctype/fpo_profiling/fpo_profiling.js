// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO Profiling", {
	async refresh(frm) {
        await hide_advance_search(frm, ['bod_kyc_name', 'name_of_cbbo', 'state_name',
            'block_name','district_name'
        ])
        await extend_options_length(frm, ['fpo_name', 'fpo_name'])
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.block_name)
	},
    state_name: async function(frm){
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
    },
    block_name: async function(frm){
        await apply_filter('block_name', 'district', frm, frm.doc.block_name)
    }
});
