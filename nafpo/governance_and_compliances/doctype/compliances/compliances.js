// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Compliances", {
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
        frm.set_value('due_date', date.toISOString().split('T')[0]);
        let due_date_2 = new Date();
        due_date_2.setDate(due_date_2.getDate() + 30);
        frm.set_value('due_date_2', due_date_2.toISOString().split('T')[0]);
        frm.set_value('due_date_3', due_date_2.toISOString().split('T')[0]);
    },
    ...['bank_statement', 'fpo_banner_with_bod_photo', 'noc', 'rent_agreement', 'electricity_bill', 'fpo_resolution'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});

frappe.ui.form.on("Governance Financial Year Child", {
    table_rmhe_add: function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        let currentDate = new Date();
        // Add one year to the current date
        let dueDate = new Date(currentDate.getFullYear() + 1, currentDate.getMonth(), currentDate.getDate());
        row.due_date = dueDate;

        currentDate.setDate(currentDate.getDate() + 60);
        row.due_date_2 = currentDate.toISOString().split('T')[0];

        let five_year_dueDate = new Date(currentDate.getFullYear() + 5, currentDate.getMonth(), currentDate.getDate());
        row.due_date_3 = five_year_dueDate.toISOString().split('T')[0];

        row.due_date_4 = dueDate;

        let fix_dueDate = new Date(currentDate.getFullYear(), 8, 30); // Months are 0-indexed, so 8 represents September
        row.due_date_5 = fix_dueDate.getFullYear() + '-09-30';
        // row.due_date_5 = '23-09-2024'

        row.due_date_6 = dueDate;
        frm.cur_grid.refresh();
    },
})
