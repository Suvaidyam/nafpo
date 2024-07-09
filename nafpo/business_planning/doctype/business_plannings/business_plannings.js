// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Business Plannings", {
    async refresh(frm) {

    },
    // fpo(frm) {
    //     frm.doc.output_side.forEach(row => {
    //         apply_filter(row.crop_name, 'fpo', frm, frm.doc.fpo)
    //     });
    // }
});

frappe.ui.form.on('Output Side Child', {
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
    },
    quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.total_harvest_by_fpo_members_quintals < row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals) {
            row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals = ''
            frappe.throw('Quantity of produce to be bought by FPO for marketing cannot exceed the total harvest by FPO members.');
        }
    }
})
