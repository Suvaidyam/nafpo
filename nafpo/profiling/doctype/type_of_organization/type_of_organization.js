// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Type of Organization", {
    refresh(frm) {
        frm.is_new() ? frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().hide()
            : frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().show()
    },
});
