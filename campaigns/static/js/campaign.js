$(document).ready(function (){

	$(document).on("click", "#show_campaign", function(){
		var checkValue = $(this);
		if(checkValue.is(":checked")){
			$("#show_campaign_table").show();
		}else{
			$("#show_campaign_table").hide();
		}
	});

});