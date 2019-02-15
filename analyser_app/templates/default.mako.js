//### This is a Mako template but for a js. The suffix is so not to confuse PyCharm.
//## ajax
$('#analyse').click(function () {
    //reset all warnings.
    $('.invalid-feedback,valid-feedback').hide();
    $('.is-invalid').removeClass('is-invalid');
    $('.is-valid').removeClass('is-valid');
    var data = new FormData();
    // deal with empty gene or mutation
    ['#gene','#missense'].map(function (id) {
        if (! $(id).val()) {$(id).addClass('is-invalid'); $(id+' ~ .invalid-feedback').show();}
    });
    data.append('gene',$('#gene').val());
    data.append('mutation',$('#mutation').val());
    $.ajax({
      type: "POST",
      url: "check_gene",
      data: data
    }).done(function() {

    });


    function addToast() {
        ``

    }


});
