$(document).ready (function() {
    $("#school").quickselect({data: schoolList});
    $("#submit").click(function(e) {
      var selectedSchool = $("#school").val();
      var numSchools = $("#numschools").val();
      if ($.inArray(selectedSchool, schoolList) == -1) {
        e.preventDefault();
        alert("You must select a valid school");
      } else if (Math.floor(numSchools) != numSchools) {
        console.log(typeof(numSchools));
        console.log(Math.floor(numSchools));
        e.preventDefault();
        alert("Please enter a valid number");
      } else {
        $("#school_form").submit()
      }
    });
  });