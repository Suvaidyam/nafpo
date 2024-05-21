// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("BOD KYC", {
	async refresh(frm) {
        await hide_advance_search(frm, ['state_name', 'fpo_name'])
        await extend_options_length(frm, ['fpo_name', 'fpo_name'])
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
	},
    state_name:async function(frm){
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo_name'])
    }
});
