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
        // frm.clear_table('table_nprj');
        if (frm.is_new()) {
            for (item of fixedCapitalItems) {
                frm.add_child('table_nprj', { 'item': item })
            }
            frm.refresh_field('table_nprj')
        }
    },
});

// frappe.ui.form.on('FPO Fixed Capital ', {
//     table_nprj_add: function (frm) {
//         console.log(frm)
//     }
// })
