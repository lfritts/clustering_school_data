$(document).ready (function() {
    $("#school").hide();
    $("#submit").hide();
    $("#reset").hide();
    $("#district").quickselect({data: districtList});
    $("#next").click(function() {
      var selectedDistrict = $("#district").val();
      if ($.inArray(selectedDistrict, districtList) == -1) {
        alert("You must select a valid district");
      } else {
        $("#next").remove();
        $("#district").remove();
        $("#school").show();
        $("#reset").show();
        $("#submit").show();
        var newLead = selectedDistrict + "<br />Now enter the name of your school";
        $(".lead").html(newLead);
      }
    });
    $("#school").quickselect({data:['School1', 'School2', 'School3']});
  });