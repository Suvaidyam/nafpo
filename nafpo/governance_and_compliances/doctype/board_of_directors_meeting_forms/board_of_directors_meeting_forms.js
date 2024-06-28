// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Board of Directors Meeting Forms", {
    async refresh(frm) {
        if (frappe.user.has_role('FPO') && frm.is_new(frm) && !frappe.user.has_role('Administrator')) {
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
        frm.fields_dict.date.$input.datepicker({ maxDate: new Date() });
        await apply_filter('fpo_member', 'fpo', frm, frm.doc.fpo)
    },
    onload: function (frm) {
        hide_list_view_in_useless_data(frm)
    },
    status(frm) {
        if (frm.doc.status == "Pending") {
            frm.set_value('date', '')
        }
    }
});
