import frappe
from frappe.utils import nowdate
from nafpo.utils.rport_filter import ReportFilter

user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
    mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
    selected_filters=['CBBO', 'IA']
)

cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""

@frappe.whitelist(allow_guest=True)
def get_fpo_profile(name=None, fields=["*"]):
    parent = frappe.db.exists({'doctype':'FPO Profiling','name_of_the_fpo':name})
    child_filter = {'parent': parent,'parenttype': 'FPO Profiling','parentfield': 'bod_kyc_name'}
    data = frappe.get_list('BOD KYC Child',
        filters=child_filter,
        fields=fields,
        page_length=10000,
        ignore_permissions = True
    )
    final_fpo_data = []
    for d in data:
        name = frappe.db.get_value('BOD KYC',d.bod_kyc,'name1')
        final_fpo_data.append(name)
    return final_fpo_data

@frappe.whitelist(allow_guest=True)
def get_fpo_profile_doc(doctype_name,filter):
    return frappe.db.get_value(doctype_name, {'name_of_the_fpo':filter },['date_of_registration'],as_dict=1)

@frappe.whitelist(allow_guest=True)
def get_exists_doc(doctype,value):
    exists = frappe.db.exists({"doctype": doctype,"fpo": value})
    return bool(exists)

# SFAC Module FPO Filter Count
@frappe.whitelist(allow_guest=True)
def get_total_eligible_fpos_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('sfac_inst', 'cbbo'), 'IA': ('sfac_inst', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    current_date = nowdate()
    query = f"""
        SELECT
            COUNT(DISTINCT sfac_inst.fpo) AS `fpo_count`
        FROM
            `tabFPO MFR 10K` AS sfac_inst
        WHERE
            sfac_inst.1st_installment_due_date <= CURDATE() {cond_str} OR
            sfac_inst.2nd_installment_due_date <= CURDATE() {cond_str} OR
            sfac_inst.3rd_installment_due_date <= CURDATE() {cond_str} OR
            sfac_inst.4th_installment_due_date <= CURDATE() {cond_str} OR
            sfac_inst.5th_installment_due_date <= CURDATE() {cond_str} OR
            sfac_inst.6th_installment_due_date <= CURDATE() {cond_str};
    """
    count = frappe.db.sql(query, {'current_date': current_date}, as_dict=False)
    return count[0][0] if count else 0

@frappe.whitelist(allow_guest=True)
def get_received_fund_before_or_on_due_date():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
        selected_filters=['CBBO', 'IA']
    )

    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    query = f"""
        SELECT COUNT(DISTINCT `fpo`)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`are_you_received_1st_installment_fund` = 'Yes' AND `1st_installment_due_date` >= `1st_installment_date` {cond_str}) OR
            (`are_you_received_2nd_installment_fund` = 'Yes' AND `2nd_installment_due_date` >= `2nd_installment_date` {cond_str}) OR
            (`are_you_received_3rd_installment_fund` = 'Yes' AND `3rd_installment_due_date` >= `3rd_installment_date` {cond_str}) OR
            (`are_you_received_4th_installment_fund` = 'Yes' AND `4th_installment_due_date` >= `4th_installment_date` {cond_str}) OR
            (`are_you_received_5th_installment_fund` = 'Yes' AND `5th_installment_due_date` >= `5th_installment_date` {cond_str}) OR
            (`are_you_received_6th_installment_fund` = 'Yes' AND `6th_installment_due_date` >= `6th_installment_date` {cond_str})
    """
    count = frappe.db.sql(query)
    return count[0][0] if count else 0

@frappe.whitelist(allow_guest=True)
def get_received_fund_after_due_date():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    query = f"""
        SELECT COUNT(DISTINCT `fpo`)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`are_you_received_1st_installment_fund` = 'Yes' AND `1st_installment_due_date` < `1st_installment_date` {cond_str}) OR
            (`are_you_received_2nd_installment_fund` = 'Yes' AND `2nd_installment_due_date` < `2nd_installment_date` {cond_str}) OR
            (`are_you_received_3rd_installment_fund` = 'Yes' AND `3rd_installment_due_date` < `3rd_installment_date` {cond_str}) OR
            (`are_you_received_4th_installment_fund` = 'Yes' AND `4th_installment_due_date` < `4th_installment_date` {cond_str}) OR
            (`are_you_received_5th_installment_fund` = 'Yes' AND `5th_installment_due_date` < `5th_installment_date` {cond_str}) OR
            (`are_you_received_6th_installment_fund` = 'Yes' AND `6th_installment_due_date` < `6th_installment_date` {cond_str})
    """
    count = frappe.db.sql(query)
    return count[0][0] if count else 0

@frappe.whitelist(allow_guest=True)
def get_Eligible_but_not_received_fund_yet():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    current_date = nowdate()
    
    query = f"""
        SELECT COUNT(DISTINCT `fpo`)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`are_you_received_1st_installment_fund` = 'No' AND `1st_installment_due_date` <= %(current_date)s {cond_str}) OR
            (`are_you_received_2nd_installment_fund` = 'No' AND `2nd_installment_due_date` <= %(current_date)s {cond_str}) OR
            (`are_you_received_3rd_installment_fund` = 'No' AND `3rd_installment_due_date` <= %(current_date)s {cond_str}) OR
            (`are_you_received_4th_installment_fund` = 'No' AND `4th_installment_due_date` <= %(current_date)s {cond_str}) OR
            (`are_you_received_5th_installment_fund` = 'No' AND `5th_installment_due_date` <= %(current_date)s {cond_str}) OR
            (`are_you_received_6th_installment_fund` = 'No' AND `6th_installment_due_date` <= %(current_date)s {cond_str})
    """
    count = frappe.db.sql(query, {'current_date': current_date})
    return count[0][0] if count and count[0] else 0

# Governance & Compliance Module FPO Filter Count
@frappe.whitelist(allow_guest=True)
def one_time_organization_registration_forms_fpo_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('no_alias', 'cbbo'), 'IA': ('no_alias', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    sql_query = f"""
        SELECT COUNT(DISTINCT `fpo`) AS count
        FROM `tabOne Time Organization Registration Forms`
        WHERE
            1=1 {cond_str}
    """
    data = frappe.db.sql(sql_query, as_dict=True)
    return data[0].count

@frappe.whitelist(allow_guest=True)
def get_annual_compliance_forms_fpo_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('ACF', 'cbbo'), 'IA': ('ACF', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    sql_query = f"""
        SELECT
            COUNT(DISTINCT sub_query.fpo_id) AS count
        FROM
            (
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS fpo_name,
                fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
                ACF.financial_year AS financial_year,
                ACF.fpo AS fpo_id,
                COUNT(*) AS total_meeting
            FROM
                `tabAnnual Compliance Forms` AS ACF
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON ACF.fpo = fpo_profiling.name_of_the_fpo
            # WHERE
            #     1=1 {cond_str}
            GROUP BY
                fpo_name, fpo_contact_number, financial_year
            HAVING
                COUNT(*) <= 3) AS sub_query
        """
    data = frappe.db.sql(sql_query, as_dict=True)
    return data[0]

@frappe.whitelist(allow_guest=True)
def get_incomplete_fpo_board_of_directors_meeting_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('bodmf', 'cbbo'), 'IA': ('bodmf', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    sql_query = f"""
        SELECT
            COUNT(DISTINCT sub_query.fpo_id) AS count
        FROM
            (
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS fpo_name,
                fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
                bodmf.financial_year AS financial_year,
                bodmf.fpo AS fpo_id,
                COUNT(*) AS total_meeting
            FROM
                `tabBoard of Directors Meeting Forms` AS bodmf
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON bodmf.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                bodmf.status = 'Completed' {cond_str}
            GROUP BY
                fpo_name, fpo_contact_number, financial_year
            HAVING
                COUNT(*) <= 3) AS sub_query
        """
    data = frappe.db.sql(sql_query, as_dict=True)
    return data[0]

@frappe.whitelist(allow_guest=True)
def get_complete_fpo_board_of_directors_meeting_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('bodmf', 'cbbo'), 'IA': ('bodmf', 'ia')},
        selected_filters=['CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    sql_query = f"""
        SELECT
            COUNT(DISTINCT sub_query.fpo_id) AS count
        FROM
            (
            SELECT
                fpo_profiling.name_of_the_fpo_copy AS fpo_name,
                fpo_profiling.contact_detail_of_fpo AS fpo_contact_number,
                bodmf.financial_year AS financial_year,
                bodmf.fpo AS fpo_id,
                COUNT(*) AS total_meeting
            FROM
                `tabBoard of Directors Meeting Forms` AS bodmf
            INNER JOIN
                `tabFPO Profiling` AS fpo_profiling ON bodmf.fpo = fpo_profiling.name_of_the_fpo
            WHERE
                bodmf.status = 'Completed' {cond_str}
            GROUP BY
                fpo_name, fpo_contact_number, financial_year
            HAVING
                COUNT(*) >= 4) AS sub_query
        """
    data = frappe.db.sql(sql_query, as_dict=True)
    return data[0]


# Aniket

@frappe.whitelist()
def membership_system_capacity_buidling_count():
    queary = """
    SELECT
        COUNT(DISTINCT CASE WHEN c.fpo IS NOT NULL THEN f.name END) AS FPO_with_Training,
        COUNT(DISTINCT CASE WHEN c.fpo IS NULL THEN f.name END) AS FPO_without_Training
    FROM tabFPO f
    LEFT JOIN tabCapacity c ON f.name = c.fpo;
    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]


@frappe.whitelist()
def get_incomplete_fpo_count():
    query = """
SELECT
    COUNT(DISTINCT fpo_profiling.name_of_the_fpo_copy) AS fpo_count
FROM
    `tabBoard of Directors Meeting Forms`
INNER JOIN
    `tabFPO Profiling` AS fpo_profiling ON `tabBoard of Directors Meeting Forms`.fpo = fpo_profiling.name_of_the_fpo
WHERE
    `tabBoard of Directors Meeting Forms`.status = 'Completed'
GROUP BY
    fpo_profiling.name_of_the_fpo_copy
HAVING
    COUNT(`tabBoard of Directors Meeting Forms`.name) <= 3
    """

    # Execute the query
    result = frappe.db.sql(query, as_dict=True)

    # Extract the count from the result
    return result[0]['fpo_count'] if result else 0



@frappe.whitelist()
def operation_system_capacity_building():
    queary = """
    SELECT 
    (SELECT COUNT(*)
     FROM (
         SELECT
             _fs.position_designation,
             _fpo.fpo_name
         FROM
             `tabCapacity` AS _cap
         INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
         INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
         INNER JOIN `tabFPO` AS _fpo ON _fs.fpo = _fpo.name
         GROUP BY _fpo.fpo_name
     ) AS has_trained) AS has_trained_count,

    (SELECT COUNT(*)
     FROM (
         SELECT
             fpo.name
         FROM
             `tabFPO` AS fpo
         WHERE
             fpo.name NOT IN (
                 SELECT DISTINCT _fs.fpo
                 FROM `tabCapacity` AS _cap
                 INNER JOIN `tabFPO Staff Select Child` AS _fssc ON _cap.name = _fssc.parent
                 INNER JOIN `tabFPO Staff` AS _fs ON _fssc.fpo_staff = _fs.name
             )
     ) AS has_not_trained) AS has_not_trained_count;


    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]


@frappe.whitelist()
def governance_system_capacity_building_count():
    queary = """
    SELECT
    COUNT(CASE WHEN subquery.training_count > 0 THEN 1 END) AS FPOs_With_Training,
    COUNT(CASE WHEN subquery.training_count = 0 THEN 1 END) AS FPOs_Without_Training
FROM (
    SELECT
        f.name AS fpo_name,
        COUNT(b.parent) AS training_count
    FROM
        `tabFPO` f
    LEFT JOIN
        `tabCapacity` c ON f.name = c.fpo
    LEFT JOIN
        `tabBOD KYC Child` b ON c.name = b.parent
    GROUP BY
        f.name
) AS subquery;
    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]



@frappe.whitelist()
def membership_system_capacity_building_fpo_mamber_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'FPO': ('_fpo', 'name')},
        selected_filters=['FPO']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""

    queary = f"""
    WITH TrainingAttendance AS (
    SELECT
        "Yes" AS attended_training,
        _fpo.name AS fpo_id
    FROM
        `tabFPO member details` AS _fmd
    INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
    WHERE
        _fmd.name IN (SELECT
            _fmdc.fpo_member
        FROM
            `tabFPO member details Child` AS _fmdc
        WHERE
            _fmdc.parenttype = 'Capacity')
    {cond_str}
    UNION ALL
    SELECT
        "No" AS attended_training,
        _fpo.name AS fpo_id
    FROM
        `tabFPO member details` AS _fmd
    INNER JOIN `tabFPO` AS _fpo ON _fmd.fpo = _fpo.name
    WHERE
        _fmd.name NOT IN (SELECT
            _fmdc.fpo_member
        FROM
            `tabFPO member details Child` AS _fmdc
        WHERE
            _fmdc.parenttype = 'Capacity')
    {cond_str}
)
SELECT
    COALESCE(SUM(CASE WHEN attended_training = 'Yes' THEN 1 ELSE 0 END), 0) AS Yes,
    COALESCE(SUM(CASE WHEN attended_training = 'No' THEN 1 ELSE 0 END), 0) AS No
FROM
    TrainingAttendance;
    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]


@frappe.whitelist()
def governance_system_capacity_building_fpo_bod_count():
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'FPO': ('_fpo', 'name')},
        selected_filters=['FPO']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""

    queary = f"""
WITH TrainingAttendance AS (
    SELECT
        "Yes" AS attended_training,
        _bk.mobile_number,
        _fpo.fpo_name,
        _bk.name1 AS bod_name
    FROM
        `tabBOD KYC` AS _bk
    INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
    WHERE
        _bk.name IN (SELECT
            _bkc.bod_kyc
        FROM
            `tabBOD KYC Child` AS _bkc
        WHERE
            _bkc.parenttype = 'Capacity')
        {cond_str}
    UNION ALL
    SELECT
        "No" AS attended_training,
        _bk.mobile_number,
        _fpo.fpo_name,
        _bk.name1 AS bod_name
    FROM
        `tabBOD KYC` AS _bk
    INNER JOIN `tabFPO` AS _fpo ON _bk.fpo_name = _fpo.name
    WHERE
        _bk.name NOT IN (SELECT
            _bkc.bod_kyc
        FROM
            `tabBOD KYC Child` AS _bkc
        WHERE
            _bkc.parenttype = 'Capacity')
    {cond_str}
)
SELECT
    SUM(CASE WHEN attended_training = 'Yes' THEN 1 ELSE 0 END) AS Yes,
    SUM(CASE WHEN attended_training = 'No' THEN 1 ELSE 0 END) AS No
FROM
    TrainingAttendance;
    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]

