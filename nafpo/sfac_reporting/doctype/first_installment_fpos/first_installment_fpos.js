// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("First Installment FPOs", {
    refresh(frm) {
        hide_advance_search(frm, ['select_fpo', 'allocation_year'])
        extend_options_length(frm, ['select_fpo', 'allocation_year'])
    },
});
