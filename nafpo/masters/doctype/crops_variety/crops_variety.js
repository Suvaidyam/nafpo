// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crops Variety", {
    async refresh(frm) {
        await apply_filter('crops_name', 'crop_type', frm, frm.doc.crops_types)
    },
    crops_types(frm) {
        apply_filter('crops_name', 'crop_type', frm, frm.doc.crops_types)
    }
});
