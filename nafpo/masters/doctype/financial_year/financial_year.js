frappe.ui.form.on("Financial Year", {
	refresh(frm) {
		hide_print_button(frm)
	},
	before_save(frm) {
		// Helper function to format date to YYYY-MM-DD
		function formatDateToYYYYMMDD(date) {
			let year = date.getFullYear();
			let month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
			let day = date.getDate().toString().padStart(2, '0');
			return `${year}-${month}-${day}`;
		}

		// Get the start year from the start date
		let startDate = new Date(frm.doc.start_date);
		let startYear = startDate.getFullYear();

		// Set the start date to 01-04-{startYear}
		let newStartDate = new Date(startYear, 3, 1); // April is month 3 (0-indexed)
		frm.doc.start_date = formatDateToYYYYMMDD(newStartDate); // format date to 'YYYY-MM-DD'

		// Set the end date to 31-03-{startYear + 1}
		let endYear = startYear + 1;
		let newEndDate = new Date(endYear, 2, 31); // March is month 2 (0-indexed), and 31st
		frm.doc.end_date = formatDateToYYYYMMDD(newEndDate); // format date to 'YYYY-MM-DD'

		// Set financial year name
		frm.doc.financial_year_name = `${startYear}-${endYear.toString().slice(-2)}`;
	}
});
