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


                % for e in ('Mutation','Effect independent of structure','Location','Nearby mutations in the population','Possible motifs','External links'):
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
        // get the sibling column of the span element that has the same text as the data-target of the selected checkboxes.
        var description = $('input:checkbox:checked')
                        .map((i,v)  => $(v).data('target'))
                        .map((i,v) => $('span:contains("'+v+'")')
                        .parent().next().html())
                        .toArray().join('\n');
        var title = '${protein.gene_name} ${mutation} <small>(${protein.recommended_name})</small>';
    });
</script>
