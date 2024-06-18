// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Six Installment Fpo", {
    refresh(frm) { },
    ...['upload_performance_report_of_the_ceo_and_accountant',
        'upload_audited_financial_statements',
        'upload_fpo_office_rent_receipt_for_last_6_months',
        'upload_output_of_business_activities_performed',
        'upload_details_of_convergence_with_any_scheme',
        'upload_has_any_retail_tie_up_been_initiated',
        'upload_whether_the_fpo_has_opened_any_store_for_sale_of_produce',
        'upload_revised_appointment_of_ceo_accountant',
        'upload_details_of_equity_grant_application_if_receivedapplied',
        'upload_list_of_shareholders_with_share_money',
        'upload_utilization_certificate_for_5th_instalment_ca_certified',
    ].reduce((acc, field) => {
        acc[field] = disable_Attachment_autosave;
        return acc;
    }, {})
});
