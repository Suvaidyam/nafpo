// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO Fixed Capital", {
    async refresh(frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            try {
                let fpo = await frappe.call({
                    method: "nafpo.apis.api.get_fpo_doc",
                    args: {
                        doctype_name: "NAFPO User",
                        value: frappe.session.user,
                    }
                });
                frm.set_value('fpo', fpo.message.fpo);
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        const fixedCapitalItems = [
            "Preoperative Expenses-Registration fee",
            "Hardware & software",
            "Weighing scale & moisture meter",
            "Office Furniture",
            "Computer & accessories"
        ];
        if (frm.is_new()) {
            if (!frm.doc.fixed_capital_details_table || frm.doc.fixed_capital_details_table.length === 0) {
                for (const item of fixedCapitalItems) {
                    frm.add_child('fixed_capital_details_table', { 'item': item });
                }
                frm.refresh_field('fixed_capital_details_table');
            }
        }
    },
});
