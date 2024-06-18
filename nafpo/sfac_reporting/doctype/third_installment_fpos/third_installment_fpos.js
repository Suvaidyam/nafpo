// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Third Installment FPOs", {
    refresh(frm) { },
    ...['upload_performance_report_of_the_ceo_and_accountant',
        'upload_audited_financial_statements',
        'upload_fpo_office_rent_receipt_for_previous_6_months',
        'upload_output_of_business_activities_performed',
        'upload_details_of_convergence_with_other_scheme',
        'upload_retail_tie_up_details',
        'upload_has_the_fpo_opened_any_store_for_sale_of_produce',
        'upload_revised_appointment_letter_of_ceo_with_increment',
        'upload_revised_appointment_letter_of_accountant_with_increment',
        'upload_details_of_equity_grant_eg_application_receivedapplied',
        'upload_list_of_shareholders_with_share_money',
        'upload_utilization_certificate_for_2nd_instalment_ca_certified',
    ].reduce((acc, field) => {
        acc[field] = disable_Attachment_autosave;
        return acc;
    }, {})
});
