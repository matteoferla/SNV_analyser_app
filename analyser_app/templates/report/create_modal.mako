#### report-btn is in header.mako, but it is shown by main.js

<div class="modal" tabindex="-1" role="dialog" id="report">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Create report</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>Choose which elements to keep (the text can be edited in a second step).</p>


                % for e in ('Mutation','Effect independent of structure','Effect based on structure','Location','Nearby mutations in the population','Possible motifs','External links'):
                    <div class="custom-control custom-switch">
                      <input type="checkbox" class="custom-control-input" id="checkbox${e.replace(' ','')}" data-target="${e}">
                      <label class="custom-control-label" for="checkbox${e.replace(' ','')}">Add &ldquo;${e}&rdquo; section</label>
                    </div>
                % endfor

          %if protein.pdbs or protein.swissmodel or protein.pdb_matches:
              <p>Choose model to use:</p>
              <select class="custom-select" id="modelSelect">
                  % for i,p in enumerate([*protein.pdbs,*protein.swissmodel,*protein.pdb_matches]):
                      <option value="${i}">${p['id']}</option>
                  % endfor
              </select>

          %endif



      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" id="create-btn">Create</button>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript">
    $('#report').on('shown.bs.modal', function (e) {
        if (myData) {
            $('#modelSelect:selected').removeAttr('selected');
            $('#modelSelect[value="'+myData.currentIndex+'"]').attr('selected','selected')
                    .html('<b>'+$('#modelSelect[value="'+myData.currentIndex+'"]').text()+'</b>');
        }
    });

    $('#create-btn').click(function () {
        // Gather data
        // get the sibling column of the span element that has the same text as the data-target of the selected checkboxes. Simple ae?
        var protein = myData.proteins[$('#modelSelect option:selected').val()];
        var description = $('input:checkbox:checked')
                        .map((i,v)  => $(v).data('target'))
                        .map((i,v) => $('span:contains("'+v+'")')
                        .parent().next().html())
                        .toArray().join('\n').replace('CURRENTCHAIN', myData.currentChain);
        var title = '${protein.gene_name} ${mutation} (${protein.recommended_name})';


        <%
            import os
            michelanglo = os.environ['MICHELANGLO_URL']
        %>
        // ask VENUS to ask Michelanglo to make a page.
        $.ajax({
        url: "/xpost",
        type: 'POST',
        dataType: 'json',
        data: {
            'description': description,
            'title': title,
            'protein': JSON.stringify(protein)
        }
        }).done(function (msg) {
            if (msg.status === 'success')
                {ops.addToast('redirect','Redirect','You are about to be redirected to '+"${michelanglo}/data/"+msg.page,'bg-info');
                window.location = "${michelanglo}/data/"+msg.page;}
            else {ops.addToast('errored','Error','Something went wrong: '+msg.status,'bg-danger');}
        }).fail(function (xhr) { //temporary.
            if (xhr.responseJSON) {
                ops.addToast('errored','Error',xhr.responseJSON.status,'bg-danger');
            } else {ops.addToast('errored','Error (are you logged in?)','bg-danger');}

        })
    });
</script>
