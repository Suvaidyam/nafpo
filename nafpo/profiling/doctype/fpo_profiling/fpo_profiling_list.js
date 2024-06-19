
frappe.listview_settings['FPO Profiling'] = {
    refresh: function (listview) {
        $('use.like-icon').hide();
        $('.list-row-activity').hide();
        $(".comment-count").hide();
        $(".frappe-timestamp").hide();
        $(".avatar-small").hide()
        $(".comment-input-wrapper").hide()
        $(".comment-input-header").hide()
        $("ql-editor").hide()
        $("ql-blank").hide()
    },
    onload: function (listview) {
        $('.layout-side-section').hide();
        $('.sidebar-section.filter-section').hide();
        $('.sidebar-section.save-filter-section').hide();
        $(".comment-input-wrapper").hide()
        $(".comment-input-header").hide()
        $("ql-editor").hide()
        $("ql-blank").hide()
    },
    // add_fields: [
    //     'name_of_the_beneficiary', 'date_of_visit', 'contact_number',
    //     'select_primary_member', 'overall_status', 'numeric_overall_status'
    // ],
    hide_name_column: true,
};