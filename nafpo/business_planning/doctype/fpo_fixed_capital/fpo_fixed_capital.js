// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO Fixed Capital", {
    refresh(frm) {
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
