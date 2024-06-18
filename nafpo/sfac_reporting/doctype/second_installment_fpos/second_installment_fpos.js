// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Second Installment FPOs", {
    refresh(frm) {

    },
    ...['upload_appointment_letter_of_ceo',
        'upload_kyc_documents_of_ceo',
        'upload_appointment_letter_of_accountant',
        'upload_fpo_registration_cost_bill',
        'upload_rent_agreement_in_the_name_of_fpo',
        'upload_rent_receipts_of_last_six_months',
        'upload_board_approved_business_plan',
        'upload_supporting_bills_for_fpo_office',
        'upload_supporting_bills_for_furniture',
        'upload_supporting_bills_for_equipment',
        'upload_supporting_bills_for_maintenance',
        'upload_letter_on_performance',
        'upload_details_of_equity_grant_application_if_applied',
        'upload_list_of_shareholders_with_shared_money_collection',
        'upload_commencement_of_business_certificate',
        'upload_utilization_certificate_for_1st_instalment_ca_certified'
    ].reduce((acc, field) => {
        acc[field] = disable_Attachment_autosave;
        return acc;
    }, {})
});
