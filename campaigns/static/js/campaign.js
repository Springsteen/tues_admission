$(document).ready(function (){

	$("#show_campaign").prop('checked', true);
	$("#show_campaign_halls").prop('checked', true);

	$(document).on("click", "#show_campaign", function(){
		var checkValue = $(this);
		if(checkValue.is(":checked")){
			$("#show_campaign_table").show();
		}else{
			$("#show_campaign_table").hide();
		}
	});

	$(document).on("click", "#show_campaign_halls", function(){
		var checkValue = $(this);
		if(checkValue.is(":checked")){
			$("#show_campaign_halls_table").show();
		}else{
			$("#show_campaign_halls_table").hide();
		}
	});

	$(document).on("click", "#search_campaign_button", function(){
		document.getElementById("search_campaign_button").disabled = true;
		var searchUrl = document.URL;
		searchUrl += "search";

		var $searchPanel = $("#campaign_search");
		var $firstName = $("#search_first_name");
		var $entryNumber = $("#search_entry_number");

		console.log("entry_number => ", $entryNumber.val(), "first_name => ", $firstName.val());

		$.getJSON(
			searchUrl,
			{"first_name" : $firstName.val(), "entry_number" : $entryNumber.val()},
			function(response){
				var searchExists = document.getElementById("search_result");
				if (searchExists == null){
					$searchPanel.append("<div id=\"search_result\">");
				}else{
					$("#search_result").remove();
					$searchPanel.append("<div id=\"search_result\">");
				}
				var $searchResultBox = $("#search_result");

				if (response.hasOwnProperty('result_set')){
					
					var html = "<table class=\"table table-hover table-stripped\">";

					html += "<thead><tr>";
					html += "<td><b>Собствено име</b></td>";
					html += "<td><b>Фамилия</b></td>";
					html += "<td><b>ЕГН</b></td>";
					html += "<td></td>";
					html += "<td></td>";
					html += "</tr></thead>";

					html += "<tbody>";
					for (id in response['result_set']){
						html += "<tr>"
						html += ("<td>" + response['result_set'][id]['first_name'] + "</td>");	
						html += ("<td>" + response['result_set'][id]['third_name'] + "</td>");	
						html += ("<td>" + response['result_set'][id]['egn'] + "</td>");	
						html += ("<td><a href=\"/campaigns/" + response['campaign_id'] + "/students/" + response['result_set'][id]['id'] + "/\" >Още данни</a></td>");	
						html += ("<td><a href=\"/campaigns/" + response['campaign_id'] + "/students/" + response['result_set'][id]['id'] + "/edit\" >Промени</a></td>");	
						html += "</tr>";
					}

					html += "</tbody></table>";
					$searchResultBox.append(html);

				}else{
					var warningExists = document.getElementById("search_warning");
					if (warningExists == null){
						$searchResultBox.append("<p id=\"search_warning\" class=\"alert alert-danger\">Не бяха намерени съвпадения.</p>");
					}
				}
			}
		);

		$firstName.val("");
		$entryNumber.val("");
	});

	$(document).on("click", "#clear_search_campaign_button", function(){
		$("#search_result").remove();
		document.getElementById("search_campaign_button").disabled = false;
	});

	$(document).on('click', '.delete-student', function (e) {
		var answer = confirm('Сигурни ли сте, че искате да изтриете този кандидат?');
		if (!answer) e.preventDefault();
	})

});
