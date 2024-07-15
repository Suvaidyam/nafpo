// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Board of Directors Meeting Forms", {
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
                set_due_date(frm);
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        frm.fields_dict.date.$input.datepicker({ maxDate: new Date() });
        await apply_filter('fpo_member', 'fpo', frm, frm.doc.fpo)
    },
    status(frm) {
        if (frm.doc.status == "Pending") {
            frm.set_value('date', '')
        }
    }
});
