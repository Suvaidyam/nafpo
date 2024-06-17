// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Board of Directors Meeting Forms", {
    async refresh(frm) {
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
