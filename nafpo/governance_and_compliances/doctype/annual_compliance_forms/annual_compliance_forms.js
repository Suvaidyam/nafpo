// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Annual Compliance Forms", {
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
        date.setFullYear(date.getFullYear() + 1);
        let formattedDate = date.toISOString().split('T')[0];
        frm.set_value('aoc_4_due_date', formattedDate);
        frm.set_value('mgt_7_due_date', formattedDate);
        frm.set_value('adt_1_due_date', formattedDate);
        frm.set_value('d_kyc_due_date', formattedDate);
        frm.set_value('it_return_due_date', formattedDate);
        frm.set_value('agm_due_date', formattedDate);
    },
    financial_year: async function (frm) {
        check_fpo(frm)
    },
    onload: function (frm) {
        hide_list_view_in_useless_data(frm)
    },
    ...['aoc_4_audit_report', 'mgt_7_director_list', 'mgt_7_shareholder_list', 'adt_1_fpo_resolution', 'd_kyc_bod_aadhar', 'd_kyc_pan_card_verification', 'd_kyc_otp', 'it_return'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});

async function check_fpo(frm) {
    let filters = {
        'financial_year': frm.doc.financial_year,
        'name': ['!=', frm.doc.name]
    };
    let fields = ['name', 'financial_year'];
    let limit = 1;

    try {
        let data = await frappe.db.get_list('Annual Compliance Forms', { filters, fields, limit });
        let exists = data.length > 0;
        if (exists) {
            await frappe.throw(`FPO already exists for the Financial Year ${frm.doc.financial_year}`);
            return false;
        }
        return true;
    } catch (err) {
        console.error('Error fetching data:', err);
        return false;
    }
}
