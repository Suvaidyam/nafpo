// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Nafpo User", {
    refresh(frm) {
        hide_advance_search(frm, ['level', 'cbbo', 'fpo', 'ia'])
        extend_options_length(frm, ['level', 'cbbo', 'fpo', 'ia'])
    },
    level: function (frm) {
        truncate_multiple_fields_value(frm, ['cbbo', 'fpo', 'ia'])
    }
});
