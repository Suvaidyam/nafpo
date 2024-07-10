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
        // frm.clear_table('fixed_capital_details_table');
        // Ensure items are added only once when the form is new
        if (frm.is_new()) {
            if (!frm.doc.fixed_capital_details_table || frm.doc.fixed_capital_details_table.length === 0) {
                for (const item of fixedCapitalItems) {
                    frm.add_child('fixed_capital_details_table', { 'item': item });
                }
                frm.refresh_field('fixed_capital_details_table');
            }
        }
        // if (frm.is_new()) {
        //     for (item of fixedCapitalItems) {
        //         frm.add_child('fixed_capital_details_table', { 'item': item })
        //     }
        //     frm.refresh_field('fixed_capital_details_table')
        // }
    },
    staff_details_table(frm) {
        console.log(frm)
    }
});

// frappe.ui.form.on('FPO Fixed Capital ', {
//     fixed_capital_details_table_add: function (frm) {
//         console.log(frm)
//     }
// })
