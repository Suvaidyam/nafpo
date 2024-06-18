// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fourth Installment FPOs", {
    refresh(frm) { },
    ...['upload_performance_report_of_the_ceo',
        'upload_fpo_office_rent_receipt_for_last_6_months',
        'upload_output_of_business_activities_performed',
        'upload_details_of_equity',
        'upload_list_of_shareholders_with_share_money',
    ].reduce((acc, field) => {
        acc[field] = disable_Attachment_autosave;
        return acc;
    }, {})
});
