$(document).ready(function(){

	$(document).on("keyup", "#id_egn", function(){
		var length = $(this).val().length;
		var warningExists = document.getElementById("id_egn_warning");
		var regexp = /(\d{10})/;
		var match = regexp.exec($(this).val());
		if (warningExists == null) {
			
				$("<div " 
					+ "id=\"id_egn_warning\"" 
					+ "class=\"alert alert-warning form_warning\">"
					+ "</div>").insertAfter(this);
			
		}
		if ((length < 10) || (match == null)) {
			$("#id_egn_warning").removeClass("alert alert-success").addClass("alert alert-warning");
			$("#id_egn_warning").text("ЕГН-то е твърде кратко или с неправилен формат");
		}else{
			$("#id_egn_warning").removeClass("alert alert-warning").addClass("alert alert-success");
			$("#id_egn_warning").text("ЕГН-то е коректно");
		}
	});

	$(document).on("keyup", ".student_grade_input", function(){
		var gradeWritten = parseInt($(this).val()) || false;
		var elemId = $(this).attr("id");
		var warningExists = document.getElementById(elemId+"_warning");
		if (warningExists == null) {
			
				$("<div " 
					+ "id=\""+ elemId +"_warning\"" 
					+ "class=\"alert alert-warning form_warning\">"
					+ "</div>").insertAfter(this);
			
		}
		if ((gradeWritten == false) || (gradeWritten < 2) || (gradeWritten > 6)) {
			$("#" + elemId + "_warning").removeClass("alert alert-success").addClass("alert alert-warning");
			$("#" + elemId + "_warning").text("Въведената оценка не е коректна");
		}else{
			$("#" + elemId + "_warning").removeClass("alert alert-warning").addClass("alert alert-success");
			$("#" + elemId + "_warning").text("Оценката е коректна");
		}
	});

});