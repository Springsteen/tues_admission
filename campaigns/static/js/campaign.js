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
		var searchUrl = document.URL;
		searchUrl += "search";

		var $searchPanel = $("#campaign_search");
		var $firstName = $("#search_first_name");
		var $egn = $("#search_egn");

		console.log("egn => ", $egn.val(), "first_name => ", $firstName.val());

		$.getJSON(
			searchUrl,
			{"first_name" : $firstName.val(), "egn" : $egn.val()},
			function(response){
				// console.log(response);
				$searchPanel.append("<div id=\"search_result\">");
				var $searchResultBox = $("#search_result");
			
				if (response.hasOwnProperty('result_set')){
							
					for (id in response['result_set']){
						// console.log(response['result_set'][id]['first_name']);
						$searchResultBox.append(response['result_set'][id]['first_name']);
						// TODO - make table with results
					}
				
				}else{
					$searchResultBox.append("nqma rezultat");
				}
			}
		);

		$firstName.val("");
		$egn.val("");
	});

	$(document).on("click", "#clear_search_campaign_button", function(){
		$("#search_result").remove();
	});

});