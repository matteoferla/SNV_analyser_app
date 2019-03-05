
window.timer;

window.addToast = function (id, title, body, bg) {
        $('#toaster').append(`<%include file="toast.mako" args="toast_id='${id}', toast_title='${title}', toast_body='${body}', toast_bg='${bg}', toast_autohide='true', toast_delay=5000 "/>`);
        $('#'+id).toast('show');
    };


window.checkGene = function (data) {
    $.ajax({
        type: "POST",
        url: "gene_check",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            if (msg.error) {halt();
                addToast('gene_error','Gene is NOT valid','<i class="far fa-exclamation-triangle"></i> The gene has NOT been matched. please correct','bg-warning');
                invalidate('#gene');}
            else {
                addToast('gene_good','Gene is valid: '+msg.uniprot_name,'<i class="far fa-check"></i> The gene has been matched','bg-info');
                return msg.uniprot_name;
            }
        })
        .fail(function () {halt();
            addToast('error_step','Error','<i class="far fa-bug"></i> An issue arose. Please review and try again','bg-danger');
            return 0
        });
};
window.i=0;
window.statusCheck = function (data) {
      i++;
      $.ajax({
        type: "POST",
        url: "task_check",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            if (msg.error) {ops.halt();
                            ops.addToast('status_error'+i,'Something went wrong.','<i class="far fa-exclamation-triangle"></i> '+msg.error,'bg-danger');
                            return 0;}
            else if (msg.unfinished > 0) {
                    ops.timer = setTimeout(function() {
                        addToast('check_status'+i,'Assembling data','<i class="fas fa-cog fa-spin"></i> <b>Ongoing tasks:</b> '+msg.status.join(', '),'bg_info');
                        statusCheck(data);
                    },1000);
                }
            else if (msg.complete) {addToast('success','Complete','<i class="far fa-check"></i> All done.','bg-success');
                get_results(data);}
            return 1;
        })
        .fail(function () {
            addToast('error_step','Error','<i class="far fa-bug"></i> An issue arose. Please review and try again','bg-danger');
            halt();
            return 0;
        });
};

window.checkMut = function (data) {
    $.ajax({
        type: "POST",
        url: "mut_check",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            if (msg.error) {
                halt();
                addToast('Mut_error','Mutation is NOT valid','<i class="far fa-exclamation-triangle"></i> The mutation has NOT been matched. please correct','bg-warning');
            }
            else {addToast('Mut_good','Mutation is valid: '+msg.uniprot_name,'<i class="far fa-check"></i> The mutation matches the sequence','bg-info');}
            return msg.uniprot_name;
        })
        .fail(function () {
            addToast('Mut_error','Error','<i class="far fa-bug"></i> An issue arose. Please review and try again','bg-danger');
            halt();
            return 0
        });
};




window.get_results = function (data)  {
    $.ajax({
        type: "POST",
        url: "get_results",
        processData: false,
        cache: false,
        contentType: false,
        data:  data
    })
        .done(function (msg) {
            $('#retrieval_card').hide(1000);
            $('#input_card').hide(1000);
            $('main').append(msg);
        })
        .fail(function () {
            addToast('res_error','Error','<i class="far fa-bug"></i> An issue arose loading the results. Please review and try again','bg-danger');
            $('#analyse').removeAttr('disabled');
            return 0;
        });
};

















//## ajax
$('#analyse').click(function () {
    $('#analyse').attr('disabled','disabled');

    //reset all warnings.
    $('.invalid-feedback,valid-feedback').hide();
    $('.is-invalid').removeClass('is-invalid');
    $('.is-valid').removeClass('is-valid');
    var data = new FormData();
    // deal with empty gene or mutation
    ['#gene','#missense'].map(function (id) {
        if (! $(id).val()) {invalidate(id); return 0;}
    });

    data.append('gene',$('#gene').val());
    data.append('mutation',$('#mutation').val());
    addToast('check_gene','Verifying input','<i class="fas fa-cog fa-spin"></i> Checking gene name matches known names and mutation is parsable...','bg-secondary');
    // checking gene.
    checkGene(data);
    // checking Mut.
    checkMut(data);
    //checking status
    timer=setTimeout(function() {statusCheck(data);},1000);
});

