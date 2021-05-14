




  $( function() {

    $( "#dialog" ).dialog({
     modal: true,
                height: 300,
                width: 500,
      autoOpen: false,
        resizable :false,
      show: {
        effect: "blind",
        duration: 500
      },
      hide: {
        effect: "blind",
        duration: 500
      },

    });
});

              $(document).on('click', '.delete' , function(event){
                event.preventDefault();

        var deletetopic= $(".deletetopic").attr('href');
        console.log(deletetopic);
         var pk = $(this).attr('value');
          console.log(pk);
        $.ajax({
                        type: 'POST',
                        url: deletetopic,
                        data: {
                        'topic_id' : pk,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){
                            console.log("worked");
                            console.log(pk);
          _html= '<div class="alert alert-success"><strong>Success!</strong> Deleted succesfully. This page will reload to save your changes.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                    window.location.reload();
                               }, 2000);


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
            });





var id;

         function dialogfunc(x,val,desc, visible) {
         id = x;
$('#dialog').dialog('option', 'title', 'Edit topic details');
            $(".username").text(val);
            $("#titleedit").val(val);
            $("#descriptionedit").val(desc);
        if(visible == "True"){
        $('#visibleedit').prop('checked', true);

        }else {
            $('#visibleedit').prop('checked', false);

        }
    console.log($('#visibleedit').val());

     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );

  }

$('#visibleedit').on('change', function(){
  $(this).val(this.checked ? "True" : "False");
})

              $(document).on('click', '#submitedits' , function(event){
                event.preventDefault();
    title=   $("#titleedit").val();
   desc = $("#descriptionedit").val();
   visible = $('#visibleedit').val();


        $.ajax({
                        type: 'POST',
                        url: '../../staff/topics/edit/'+id+'/',
                        data: {
                        'topic_id' : id,
                        'title' :title,
                        'desc' :desc ,
                        'visible' :visible,
                        'csrfmiddlewaretoken': csrftoken
                        },

                        success: function(response){
                        console.log(response);
                         $('#dialog').dialog('close');
                    _html= '<div class="alert alert-success"><strong>Success!</strong> Edited successfully. This page will reload to save your changes.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                    window.location.reload();
                               }, 2000);


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
            });









              $(document).on('click', '#undo' , function(event){
                event.preventDefault();
var undotopic= $(".undotopic").attr('href');
var id = $(this).val();
console.log(undotopic);
        $.ajax({
                        type: 'POST',
                        url: undotopic,
                        data: {
                        'topic_id' : id,
                        'csrfmiddlewaretoken': csrftoken
                        },

                        success: function(response){
                        console.log(response);
                         $('#dialog').dialog('close');
                    _html= '<div class="alert alert-success"><strong>Success!</strong> Undo successfully. This page will reload to save your changes.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                    window.location.reload();
                               }, 2000);


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
            });
