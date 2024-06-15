// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("IA", {
    refresh(frm) {

    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
});
