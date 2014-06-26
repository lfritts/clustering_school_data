$(document).ready (function() {
    $("#school").quickselect({data: schoolList});
    $("#submit").click(function() {
      var selectedSchool = $("#school").val();
      if ($.inArray(selectedSchool, schoolList) == -1) {
        alert("You must select a school");
      } else {
        $("#school_form").submit()
      }
    });
  });