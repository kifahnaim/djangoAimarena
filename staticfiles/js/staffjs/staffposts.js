var pid ;
    function deleteconfirm(id, post){
     $( "#my_dialog" ).css("display", "block");
     $("#text").text("Are you sure you want to delete " + post );
     pid = id;

$( "#my_dialog" ).dialog( "open" );

}

function undopost(id){

                event.preventDefault();

                var undourl = $("#undourl").attr("href");
                $.ajax({
                    type: 'POST',
                    url: '../../staff/posts/undo/'+id+'/',
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> Post undo succesfully.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                window.location.reload();
                                   $('#success').fadeOut();
                               }, 2000);


                        console.log("undo worked");

                    },
                    error: function(rs, e){

                        console.log("not");
                    },
            });





}


function closepost(id){
                console.log(id);
                event.preventDefault();

                var pk = $(this).attr('value');
                var btn =$("#open");

                var closeurl = $("#closeurl").attr("href");
                 console.log(closeurl);
                $.ajax({
                    type: 'POST',
                    url: '../../staff/posts/close/'+id+'/',
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> Post closed succesfully.</div>';
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


function openpost(id){
                console.log(id);
                event.preventDefault();

                var pk = $(this).attr('value');
                var btn =$("#open");

                var openurl = $("#openurl").attr("href");
                 console.log(openurl);
                $.ajax({
                    type: 'POST',
                    url: '../../staff/posts/open/'+id+'/',
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftoken
                     },
                    dataType: 'json',
                    success: function(response){

           _html= '<div class="alert alert-success"><strong>Success!</strong> Post closed succesfully.</div>';
                             $("#success").append(_html);


                       setTimeout(function() {
                                window.location.reload();

                                   $('#success').fadeOut();
                               }, 2000);


                        console.log("open worked");

                    },
                    error: function(rs, e){

                        console.log("not");
                    },
            });





}





var pos = { my: "center center", at: "center center", of: window };
$(function() {
   $( "#my_dialog" ).dialog({
   	autoOpen: false,
   position:pos,
    show: {
     effect: "fade",
     duration: 500
     },
    hide: {
     effect:"size",
     duration:200
     },
    buttons: {

     "Sure ": {
     class: 'rightButton',
      text : 'Sure',
      id: "sure",

     click: function() {
        ajaxcall(pid);
     }

     },


        "Close":{
        class :'leftButton',
        text : 'close',
       click: function() {

     $( this ).dialog( "close" );
     }

    }}
		});
});











function ajaxcall(pid)
{
console.log(pid);
deleteurl = $("#deleteurl").attr("href");
 $.ajax({
                        type: 'POST',
                        url: '../../staff/posts/delete/'+pid+'/',
                        data: {

                        'post_id' : pid,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){



                            console.log("success");
                            $( "#my_dialog" ).dialog( "close" );

                            _html= '<div class="alert alert-success"><strong>Success!</strong> Deleted succesfully.</div>';
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





}

