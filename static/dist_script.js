$(document).ready (function() {
    $("#district").quickselect({data: districtList});
    $("#submit").click(function() {
      var selectedDistrict = $("#district").val();
      if ($.inArray(selectedDistrict, districtList) == -1) {
        alert("You must select a valid district");
      } else {
        $("#dist_form").submit()
      }
    });
    // $("#school").quickselect({data:['School1', 'School2', 'School3']});
  });