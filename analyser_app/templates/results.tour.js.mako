<script type="text/javascript">
//tour
    window.tutorial = new Tour({
            steps: [{
                element: '#user_text',
                title: 'User Text',
                content: 'This part is a rendered markdown text read from a file Matteo put in the folder `data/manual`.',
                placement: 'top'
            },{
                element: '#fv',
                title: 'Feature viewer',
                content: 'This section shows the parts of the gene. Clicking on one will highlight it in the structure panel',
                placement: 'right'
            },{
                element: '#viewport',
                title: 'Protein viewer',
                content: 'This sections shows the protein structure, which can be interacted with by dragging with one of the three mouse buttons.<br/><img src="https://www.well.ox.ac.uk/~matteo/clickmap.jpg" width="100%">',
                placement: 'left'
            }],
            backdrop: true
        });
    tutorial.init();

    $('#guide').click(function () {
        tutorial.restart();
    });
</script>
