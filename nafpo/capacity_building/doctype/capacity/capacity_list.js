
frappe.listview_settings['Capacity'] = {
    refresh: function (listview) {
        $('use.like-icon').hide();
        $('.list-row-activity').hide();
        $(".comment-count").hide();
        $(".frappe-timestamp").hide();
        $(".avatar-small").hide()
        $("ql-editor").hide()
        $("ql-blank").hide()
    },
    onload: function (listview) {
        $('.layout-side-section').hide();
        $('.sidebar-section.filter-section').hide();
        $('.sidebar-section.save-filter-section').hide();
        $("ql-editor").hide()
    }
};