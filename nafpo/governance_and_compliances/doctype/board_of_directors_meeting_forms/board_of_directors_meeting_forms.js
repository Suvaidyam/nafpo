// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
async function check_fpo_profile(frm) {
    let response = await frappe.call({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: "FPO Profiling",
            filterName: "name_of_the_fpo",
            value: frm.doc.fpo,
        }
    });
    if (response.message == undefined) {
        // frm.set_value('fpo', '')
        return frappe.throw({ message: 'Please Create FPO Profiling for this FPO' });
    }
}
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
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        hide_print_button(frm)
        await apply_filter('fpo_member', 'fpo', frm, frm.doc.fpo)
        frm.fields_dict.date.$input.datepicker({ maxDate: new Date() });
    },
    status(frm) {
        if (frm.doc.status == "Pending") {
            frm.set_value('date', '')
        }
    },
    fpo(frm) {
        check_fpo_profile(frm)
    }
});
