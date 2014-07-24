$( document ).ready(function() {
    $('.dropdown').hide();
    $('span').click(
        function (event) {
            var target = $(event.target);
            var dd_id = target.attr('data-dd-id');
            var dd_el = $('#' + dd_id)
            dd_el.slideToggle();
        })
});