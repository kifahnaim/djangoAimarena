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

    function deletenews(id){
                    $.ajax({
                    type: 'POST',
                    url: '../../staff/managenews/delete/'+id+'/',
                    data: {
                    'news_id':id,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> News deleted succesfully.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                window.location.reload();
                                   $('#success').fadeOut();
                               }, 2000);


                        console.log("close worked");

                    },
                    error: function(rs, e){

                        console.log("not");
                    },
            });

    }


        function undonews(id){
                    $.ajax({
                    type: 'POST',
                    url: '../../staff/managenews/undo/'+id+'/',
                    data: {
                    'news_id':id,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> News restored succesfully.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                window.location.reload();
                                   $('#success').fadeOut();
                               }, 2000);


                        console.log("close worked");

                    },
                    error: function(rs, e){

                        console.log("not");
                    },
            });

    }

var editid ;
function editnews(id ,news ){

editid = id;
     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );
$("#newsedit").val(news);
}

function submitedits(){


newsedit = $("#newsedit").val();

                $.ajax({
                    type: 'POST',
                    url: '../../staff/managenews/edit/'+editid+'/',
                    data: {
                    'news_id':editid,
                    'newsedit': newsedit,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> News edited succesfully.</div>';
                             $("#success").append(_html);
                       $('#dialog').dialog('close');
                               setTimeout(function() {
                                window.location.reload();
                                   $('#success').fadeOut();
                               }, 2000);


                        console.log("close worked");

                    },
                    error: function(rs, e){

                        console.log("not");
                    },
            });










}