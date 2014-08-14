$(document).ready (function() {
    $("#district").quickselect({data: districtList});
    $("#submit").click(function(e) {
      var selectedDistrict = $("#district").val();
      if ($.inArray(selectedDistrict, districtList) == -1) {
        e.preventDefault();
        alert("You must select a valid district");
      } else {
        $("#dist_form").submit()
      }
    });
  });