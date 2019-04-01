//### This (default.mako.js is a Mako template but for a js. The suffix is so not to confuse PyCharm.
window.invalidate = function (id) {
    $(id).removeClass('is-valid');
    $(id).addClass('is-invalid');
    $(id+' ~ .valid-feedback').hide();
    $(id+' ~ .invalid-feedback').show();
};

window.ops={timer: null, i: 0};

ops.addToast = function (id, title, body, bg) {
        $('#toaster').append(`<%include file="toast.mako" args="toast_id='${id}', toast_title='${title}', toast_body='${body}', toast_bg='${bg}', toast_autohide='true', toast_delay=5000 "/>`);
        $('#'+id).toast('show');
    };

ops.halt = function () {
    clearTimeout(ops.timer);
    $('#analyse').removeAttr('disabled');
    setTimeout(ops.halt,100);
};

ops.reset_warnings = function () {
    $('.invalid-feedback,valid-feedback').hide();
    $('.is-invalid').removeClass('is-invalid');
    $('.is-valid').removeClass('is-valid');
};

ops.analyse = function (data)  {
    $.ajax({
        type: "POST",
        url: "analyse",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            ops.halt();
            if (msg.error) {ops.addToast('res_error','Error','<i class="far fa-bug"></i> An issue arose analysing the results.<br/>'+msg.error,'bg-danger');}
            else {
                $('#retrieval_card').hide(1000);
            $('#input_card').hide(1000);
            $('main').append(msg);
            $('#new_analysis').show();
            }
        })
        .fail(function () {
            ops.halt();
            ops.addToast('res_error','Error','<i class="far fa-bug"></i> An issue arose loading the results. Please review and try again','bg-danger');
            $('#analyse').removeAttr('disabled');
            return 0;
        });
};

$('#reset').click(function () {
    ops.halt();
    ops.reset_warnings();
    $('#gene').val('');
    $('#mutation').val('');
    throw new Error("User requested halt");
});

$('#demo').click(function () {
    $.ajax({type: 'POST',
            url: 'get_random'}).done(function (msg) {
        $('#gene').val(msg.name);
        $('#mutation').val(msg.mutation);
    });
});

ops.statusCheck = function (data) {
      ops.i++; // user for unique ids
      var i=ops.i;
      $.ajax({
        type: "POST",
        url: "task_check",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            if (msg.error) {
                ops.halt();
                ops.addToast('status_error'+i,'Something went wrong.','<i class="far fa-exclamation-triangle"></i> '+msg.error,'bg-danger'); return 0;}
            else if (msg.complete) {ops.addToast('status_complete'+i,'Complete','<i class="far fa-check"></i> '+msg.status,'bg-success');}
                else { ops.timer = setTimeout(function() {
                        ops.addToast('status_ongoing'+i,'Analysis','<i class="far fa-cog fa-spin"></i> '+msg.status,'bg-info');
                        ops.statusCheck(data);
                    },1000);}
            return 1;
        })
        .fail(function () {
            ops.addToast('error_step'+i,'Error','<i class="far fa-bug"></i> An issue arose. Please review and try again','bg-danger');
            ops.halt();
            return 0;
        });
};

//## request
$('#analyse').click(function () {
    $('#analyse').attr('disabled','disabled');
    //reset all warnings.
    ops.reset_warnings();
    var data = new FormData();
    // deal with empty gene or mutation
    ['#gene','#missense'].map(function (id) {
        if (! $(id).val()) {invalidate(id); return 0;}
    });

    data.append('gene',$('#gene').val());
    data.append('mutation',$('#mutation').val());
    ops.addToast('check_gene','Verifying input','<i class="fas fa-cog fa-spin"></i> Checking gene name matches known names and mutation is parsable...','bg-secondary');
    // checking gene.
    ops.analyse(data);
    //checking status
    timer=setTimeout(function() {ops.statusCheck(data);},1000);
});
