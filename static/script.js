$("#district").quickselect({data:['Option1', 'Option2', 'Option3']});
$("#school").quickselect({data:['School1', 'School2', 'School3']});
$("#district").select(function() {alert($("#district").val());});
// $("#district").on('change keyup paste mouseup', function() {alert("Change detected!");});