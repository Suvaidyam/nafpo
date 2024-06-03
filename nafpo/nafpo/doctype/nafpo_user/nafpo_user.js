// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt


//   get permissions
const get_permission = async (user) => {
    let list = await callAPI({
        method: 'nafpo.apis.user.get_user_permission',
        freeze: true,
        args: {
            doctype: "User Permission",
            user: user,
            view: "List",
            order_by: "",
            group_by: '',
        },

        freeze_message: __("Getting Permissions"),
    })
    return list
}

const render_tables = async (frm) => {
    let list = await get_permission(frm.doc.email)
    let tables = `<table class="table">
    <thead>
        <tr>
            <th scope="col">Sr.No</th>
            <th scope="col">Doctype</th>
            <th scope="col">Value</th>
        </tr>
    </thead>
    <tbody>
    `
    for (let i = 0; i < list?.length; i++) {
        tables = tables + `
        <tr>
            <th scope="row">${i + 1}</th>
            <td>${list?.[i].allow}</td>
            <td>${list?.[i].name_value}</td>
        </tr>
            `
    }
    tables = tables + `</tbody>
    </table>`;
    document.getElementById('datatable').innerHTML = list?.length ? tables : '';
}

frappe.ui.form.on("Nafpo User", {
    async refresh(frm) {
        !frm.is_new() && await render_tables(frm);
        hide_advance_search(frm, ['level', 'cbbo', 'fpo', 'ia'])
        extend_options_length(frm, ['level', 'cbbo', 'fpo', 'ia'])
    },
    level: function (frm) {
        truncate_multiple_fields_value(frm, ['cbbo', 'fpo', 'ia'])
    }
});
