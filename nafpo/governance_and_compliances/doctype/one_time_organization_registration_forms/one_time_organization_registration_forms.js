// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("One Time Organization Registration Forms", {
    refresh: async function (frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            try {
                let { message: { fpo } } = await frappe.call({
                    method: "frappe.client.get",
                    args: { doctype: "Nafpo User", name: frappe.session.user }
                });
                frm.set_value('fpo', fpo)
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        let date = new Date();
        date.setDate(date.getDate() + 180);
        frm.set_value('inc_20_due_date', date.toISOString().split('T')[0]);
        date.setDate(date.getDate() + 30);
        frm.set_value('inc_22_due_date', date.toISOString().split('T')[0]);
        frm.set_value('adt_1_due_date', date.toISOString().split('T')[0]);
    },
    financial_year: async function (frm) {
        check_fpo(frm)
    },
    ...['inc_20_bank_statement', 'inc_20_bank_statement', 'inc_22_noc', 'inc_22_rent_agreement', 'inc_22_electricity_bill', 'adt_1_fpo_resolution'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});

async function check_fpo(frm) {
    let filters = {
        'financial_year': frm.doc.financial_year,
        'name': ['!=', frm.doc.name] // Exclude current document
    };
    let fields = ['name', 'financial_year'];
    let limit = 1;

    try {
        let data = await frappe.db.get_list('One Time Organization Registration Forms', { filters, fields, limit });
        let exists = data.length > 0;
        if (exists) {
            await frappe.throw(`FPO already exists for the Financial Year ${frm.doc.financial_year}`);
            return false; // Prevent form from saving
        }
        return true; // Allow form to save
    } catch (err) {
        console.error('Error fetching data:', err);
        return false; // Prevent form from saving on error
    }
}