





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

$("#editvisible").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }
});
$("#editonlystaff").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }
});
 $("#editpinned").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }});
  $("#editacceptedstaff").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }});
   $("#editrejectedstaff").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }});

    $("#editacceptedappeal").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }});

     $("#editrejectedappeal").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'True');
  } else {
    $(this).attr('value', 'False');
  }});









var id;

         function dialogfunc(x,val,desc, visible,pinned, staffacc, staffrej, accappeal, rejappeal, isvisible) {
         id = x;
$('#dialog').dialog('option', 'title', 'Edit topic details');
            $(".username").text(val);
            $("#editsubtitle").val(val);
            $("#editsubdescription").val(desc);


             if (isvisible == "False")
             {
                     $('#editonlystaff').prop('checked', true);
                       $('#editonlystaff').attr('value', 'True');
              }
              else {
                     $('#editonlystaff').prop('checked', false);
                     $('#editonlystaff').attr('value', 'False');
              }

          if(visible == "True"){
        $('#editvisible').prop('checked', true);
       $('#editvisible').attr('value', 'True');
        }else {
            $('#editvisible').prop('checked', false);
  $('#editvisible').attr('value', 'False');
        }
            if(pinned == "True"){
        $('#editpinned').prop('checked', true);
$('#editpinned').attr('value', 'True');
        }else {
            $('#editpinned').prop('checked', false);
  $('#editpinned').attr('value', 'False');
        }

         if(staffacc == "True"){
        $('#editacceptedstaff').prop('checked', true);
$('#editacceptedstaff').attr('value', 'True');
        }else {
            $('#editacceptedstaff').prop('checked', false);
  $('#editacceptedstaff').attr('value', 'False');
        }
             if(staffrej == "True"){
        $('#editrejectedstaff').prop('checked', true);
$('#editrejectedstaff').attr('value', 'True');
        }else {
            $('#editrejectedstaff').prop('checked', false);
  $('#editrejectedstaff').attr('value', 'False');
        }

        if(accappeal == "True"){
        $('#editacceptedappeal').prop('checked', true);
$('#editacceptedappeal').attr('value', 'True');
        }else {
            $('#editacceptedappeal').prop('checked', false);
  $('#editacceptedappeal').attr('value', 'False');
        }

                if(rejappeal == "True"){
        $('#editrejectedappeal').prop('checked', true);
$('#editrejectedappeal').attr('value', 'True');
        }else {
            $('#editrejectedappeal').prop('checked', false);
  $('#editrejectedappeal').attr('value', 'False');
        }

     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );

  }


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
                        'csrfmiddlewaretoken':csrftoken
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





    $(document).on('click', '#submiteditsdialog' , function(event){
                event.preventDefault();



    title= $("#editsubtitle").val();
    desc = $("#editsubdescription").val();
visible = $('#editvisible').val();
pinned = $('#editpinned').val();


editonlystaff = $('#editonlystaff').val();
acceptedstaff =$('#editacceptedstaff').val();
rejectedstaff =$('#editrejectedstaff').val();
acceptedappeal = $('#editacceptedappeal').val();
rejectedappeal =$('#editrejectedappeal').val();
dropdowntopics =$("#dropdowntopicsedit option:selected").val()
        $.ajax({
                        type: 'POST',
                        url: '../../staff/subtopics/edit/'+id+'/',
                        data: {
                        'topic_id' : id,
                        'title' :title,
                        'desc' :desc ,
                        'visible' :visible,
                        'pinned' :pinned,
                        'editonlystaff':editonlystaff,
                        'acceptedstaff' :acceptedstaff,
                        'rejectedstaff' :rejectedstaff,
                        'acceptedappeal' :acceptedappeal,
                        'rejectedappeal' :rejectedappeal,
                        'dropdowntopics':dropdowntopics,
                        'csrfmiddlewaretoken':csrftoken
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