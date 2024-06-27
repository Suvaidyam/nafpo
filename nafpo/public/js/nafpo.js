
frappe.router.on('change', async () => {
    let cur_router = await frappe.get_route();
    if (cur_router[0] === 'Workspaces') {
        $('.sidebar-toggle-btn').show();
        $('.layout-side-section').show();
    } else {
        $('.sidebar-toggle-btn').hide();
        $('.layout-side-section').hide();
    }
});
