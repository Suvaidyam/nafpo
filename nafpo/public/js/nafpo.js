
frappe.router.on('change', async () => {
    let cur_router = await frappe.get_route()
    // console.log(cur_router, "oluiupou")
    if (["FPO Profiling","BOD KYC","Producer Groups","FPO member details","State","District","Block","Grampanchayat","Village","IA"].includes(cur_router[1])) {
        $('.sidebar-toggle-btn').hide()
        $('.layout-side-section').hide();
    } else {
        $('.sidebar-toggle-btn').show()
        $('.layout-side-section').show();
    }
});