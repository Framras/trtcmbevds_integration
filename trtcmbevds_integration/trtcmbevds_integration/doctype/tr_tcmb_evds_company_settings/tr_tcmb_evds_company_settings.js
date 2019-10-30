// Copyright (c) 2019, Framras AS-Izmir and contributors
// For license information, please see license.txt

frappe.ui.form.on('TR TCMB EVDS Company Settings', {
	// refresh: function(frm) {

	// }
		test_integration: function(frm){
	    if(frm.doc.key!=""){
	        frappe.call({
	            method: "trtcmbevds_integration.api.test_integration",
	            args:{
	                testtoken: frm.doc.key
	            },
	            callback: function(r){
                    frm.set_value("integrationresult", r.message)
	            }
	        })
	    }
	}
});
