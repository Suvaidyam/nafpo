
frappe.listview_settings['First Installment FPOs'] = {
    refresh: function () {
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
    onload: function () {
        $('.layout-side-section').hide();
        $('.sidebar-section.filter-section').hide();
        $('.sidebar-section.save-filter-section').hide();
        $(".comment-input-wrapper").hide()
        $(".comment-input-header").hide()
        $("ql-editor").hide()
        $("ql-blank").hide()
    }
};