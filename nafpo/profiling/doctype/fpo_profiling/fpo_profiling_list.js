
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
    add_fields: [
        'fpo', 'state_name', 'district_name', 'name_of_the_fpo', 'cbbo', 'type_of_organization', 'date_of_incorporation'
    ],
    hide_name_column: true,
};