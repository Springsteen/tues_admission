$(document).ready(function(){

    $(document).on("click", ".transaction_btn", function() {
        $(this).prop("disabled", true);
    });

    /* CREATE STUDENT FORM */

    var createStudentButtonExists = document.getElementById("create_student_submit");

    if (createStudentButtonExists != null) {
        createStudentButtonExists.disabled = true;

        setInterval(
            function(){
                var firstNameLength = $("#id_first_name").val().length;
                var secondNameLength = $("#id_second_name").val().length;
                var thirdNameLength = $("#id_third_name").val().length;
                var egnLength = $("#id_egn").val().length;
                if ((firstNameLength > 0) && (secondNameLength > 0) &&
                    (thirdNameLength > 0) && (egnLength > 0)
                ){
                    createStudentButtonExists.disabled = false;
                }else{
                    createStudentButtonExists.disabled = true;
                }
            },
            5000
        );
    }

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

    $(document).on("click", ".required_field", function(){
        var elemId = $(this).attr("id");
        var warningExists = document.getElementById(elemId+"_warning");
        if(warningExists == null) {
            $("<div "
                + "id=\""+ elemId +"_warning\""
                + "class=\"alert alert-warning form_warning\">"
                + "Това поле е задължително</div>").insertAfter(this);
        }
    });

    $(document).on("click", ".student_choices", function(){
        var elemId = $(this).attr("id");
        var warningExists = document.getElementById(elemId+"_warning");
        if(warningExists == null){
            $("<div "
                + "id=\""+ elemId +"_warning\""
                + "class=\"alert alert-warning form_warning\">"
                + "Въведете СП или КМ</div>").insertAfter(this);
        }
    });

    /* CREATE CAMPAIGN FORM */

    var createCampaignButtonExists = document.getElementById("create_campaign_submit");

    if (createCampaignButtonExists != null){
        createCampaignButtonExists.disabled = true;

        setInterval(
            function(){
                var titleLength = $("#id_title").val().length;
                var descriptionLength = $("#id_description").val().length;

                if((titleLength > 0) && (descriptionLength > 0)){
                    createCampaignButtonExists.disabled = false;
                }else{
                    createCampaignButtonExists.disabled = true;
                }
            },
            3000
        );
    };

    $('#edit_student_next').on('click', function (e) {
        $('#create_student_form').find('[name="next"]').val('true');
    });

});
