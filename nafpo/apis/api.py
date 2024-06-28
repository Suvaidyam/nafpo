import frappe
from frappe.utils import nowdate
@frappe.whitelist()
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

@frappe.whitelist()
def get_fpo_profile_doc(doctype_name,filter):
    return frappe.db.get_value(doctype_name, {'name_of_the_fpo':filter },['date_of_registration'],as_dict=1)

@frappe.whitelist()
def get_total_eligible_fpos_count():
    current_date = nowdate()
    query = """
        SELECT COUNT(*)
        FROM `tabFPO MFR 10K`
        WHERE `1st_installment_due_date` <= %(current_date)s
        OR `2nd_installment_due_date` <= %(current_date)s
        OR `3rd_installment_due_date` <= %(current_date)s
        OR `4th_installment_due_date` <= %(current_date)s
        OR `5th_installment_due_date` <= %(current_date)s
        OR `6th_installment_due_date` <= %(current_date)s
    """
    count = frappe.db.sql(query, {'current_date': current_date}, as_dict=False)
    return count[0][0] if count else 0

@frappe.whitelist()
def get_received_fund_before_or_on_due_date():
    current_date = nowdate()
    query = """
        SELECT COUNT(*)
        FROM `tabFPO MFR 10K`
        WHERE `1st_installment_due_date` <= %(current_date)s
        OR `2nd_installment_due_date` <= %(current_date)s
        OR `3rd_installment_due_date` <= %(current_date)s
        OR `4th_installment_due_date` <= %(current_date)s
        OR `5th_installment_due_date` <= %(current_date)s
        OR `6th_installment_due_date` <= %(current_date)s
    """
    count = frappe.db.sql(query, {'current_date': current_date}, as_dict=False)
    return count[0][0] if count else 0

@frappe.whitelist()
def get_received_fund_before_or_on_due_date():
    current_date = nowdate()
    query = """
        SELECT COUNT(*)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`are_you_received_1st_installment_fund` = 'Yes' AND `1st_installment_due_date` >= `1st_installment_date`) OR
            (`are_you_received_2nd_installment_fund` = 'Yes' AND `2nd_installment_due_date` >= `2nd_installment_date`) OR
            (`are_you_received_3rd_installment_fund` = 'Yes' AND `3rd_installment_due_date` >= `3rd_installment_date`) OR
            (`are_you_received_4th_installment_fund` = 'Yes' AND `4th_installment_due_date` >= `4th_installment_date`) OR
            (`are_you_received_5th_installment_fund` = 'Yes' AND `5th_installment_due_date` >= `5th_installment_date`) OR
            (`are_you_received_6th_installment_fund` = 'Yes' AND `6th_installment_due_date` >= `6th_installment_date`)
    """
    count = frappe.db.sql(query)
    return count[0][0] if count else 0

@frappe.whitelist()
def get_received_fund_after_due_date():
    current_date = nowdate()
    query = """
        SELECT COUNT(*)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`status` = 'Completed' AND `1st_installment_due_date` <= `1st_installment_date`)
    """
    count = frappe.db.sql(query)
    return count[0][0] if count else 0

@frappe.whitelist()
def get_Eligible_but_not_received_fund_yet():
    current_date = nowdate()
    query = """
        SELECT COUNT(*)
        FROM `tabFPO MFR 10K`
        WHERE 
            (`are_you_received_1st_installment_fund` = 'No' AND `1st_installment_due_date` <= %(current_date)s) OR
            (`are_you_received_2nd_installment_fund` = 'No' AND `2nd_installment_due_date` <= %(current_date)s) OR
            (`are_you_received_3rd_installment_fund` = 'No' AND `3rd_installment_due_date` <= %(current_date)s) OR
            (`are_you_received_4th_installment_fund` = 'No' AND `4th_installment_due_date` <= %(current_date)s) OR
            (`are_you_received_5th_installment_fund` = 'No' AND `5th_installment_due_date` <= %(current_date)s) OR
            (`are_you_received_6th_installment_fund` = 'No' AND `6th_installment_due_date` <= %(current_date)s)
    """
    count = frappe.db.sql(query, {'current_date': current_date})
    return count[0][0] if count and count[0] else 0


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
def operation_system_capacity_building():
    queary = """
    SELECT COUNT(*) as count, 'Yes' as has_trained
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
) AS has_trained

UNION ALL

SELECT COUNT(*) as count, 'No' as has_trained
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
) AS has_not_trained;

    """
    count= frappe.db.sql(queary, as_dict=1)
    return count[0]
@frappe.whitelist()
def get_incomplete_fpo_board_of_directors_meeting_count():
    query = """
        SELECT
            COUNT(*) AS fpo_count
        FROM (
            SELECT
                fpo
            FROM
                `tabBoard of Directors Meeting Forms`
            WHERE
                `status` = 'Completed'
            GROUP BY
                fpo
            HAVING
                COUNT(*) <= 3
        ) AS subquery
    """

    # Execute the query
    result = frappe.db.sql(query, as_dict=True)

    # Extract the count from the result
    return result[0]['fpo_count'] if result else 0

