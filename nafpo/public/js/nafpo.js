
frappe.router.on('change', async () => {
    let cur_router = await frappe.get_route();
    if (cur_router[0] === 'Workspaces') {
        $('.sidebar-toggle-btn').show();
        $('.layout-side-section').show();
        // $('.custom-actions').hide();
    } else {
        $('.sidebar-toggle-btn').hide();
        $('.layout-side-section').hide();
        // $('.custom-actions').hide();
    }
    if (cur_router.length == 2 && !frappe.user_roles.includes("System Manager", "Administrator")) {
        if (cur_router[0] == "Workspaces") {
            $("#page-Workspaces .page-actions").html("")
        }
    }
});
