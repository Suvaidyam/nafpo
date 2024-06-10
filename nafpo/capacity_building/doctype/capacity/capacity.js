// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt


frappe.ui.form.on("Capacity", {
    refresh: async function (frm) {
        // if (frappe.user.has_role('FPO')) {
        //     try {
        //         let { message: { fpo } } = await frappe.call({
        //             method: "frappe.client.get",
        //             args: { doctype: "Nafpo User", name: frappe.session.user }
        //         });
        //         frm.set_value('fpo', fpo)
        //     } catch (e) {
        //         console.error('User data fetch error:', e);
        //     }
        // }
    },
    async fpo(frm) {
        let data = await callAPI({
            method: "nafpo.apis.api.get_fpo_profile",
            args: {
                name: frm.doc.fpo,
            }
        })
        console.log('data :>> ', data);
        frm.set_value('bod_kyc_name', data)
    },
    start_date(frm) {
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        frm.set_value('total_days', total_days)
        frm.set_df_property('total_days', 'read_only', true);
    },
    end_date(frm) {
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        frm.set_value('total_days', total_days)
        frm.set_df_property('total_days', 'read_only', true);
    }
});
