
$( document ).ready(function() {

    showComment= function(){
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.remove("hide");
}

   hidecomment=function(){
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.toggle("hide");
}


togglereplies=function(){
    var replyArea = document.getElementsById("reply-content");
    replyArea.classList.add("hide");
}

showreply= function(){
    var ReplySection = document.getElementById("replysection");
    ReplySection.classList.remove("hide");

    var ReplyCancel = document.getElementById("replycancel");
    ReplyCancel.classList.remove("hide");


}



hidereply= function(){
    var ReplySection = document.getElementById("replysection");
    ReplySection.classList.add("hide");


    var ReplyCancel = document.getElementById("replycancel");
    ReplyCancel.classList.add("hide");
}
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

$( "#replytoggler" ).click(function() {
    $(".reply-bubble").slideToggle("slow");

});

$("#replytoggler").css({cursor: "pointer"});





    $(document).on('submit', '.comment-form', function(event){
        event.preventDefault();
        console.log($(this).serialize());
        $ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                $('.main-comment-section').html(response['form']);
                $('textarea').val('');
                $('.reply-btn').click(function() {
                    $(this).parent().parent().next('.replied-comments').fadeToggle();
                    $('textarea').val('');
                    window.location.reload();

                });
            },
            error: function(rs, e) {
                console.log(rs.responseText);
            },
        });
    });



    $("textarea").css({width: "100%"});


    $("textarea").css({float: "center"});

    $("textarea").css({opacity: "0.8"});

    $(".customized").css({opacity: "0"});





    $( "#commentui" ).click(function() {
        $( "#commentmain" ).slideDown("500");
});


$( "#cancelcomment" ).click(function() {
        $( "#commentmain" ).slideUp("500");
});










    $(function(){
        $("textarea").focusin(
            function(){
         customizedbtn = $("#replysubmit").parent().find(".customized");
         console.log(customizedbtn);
             $(this).parent().find(".customized").animate({opacity: "1"});
                $(this).css({opacity: "1"});

            },

        );

          $("textarea").focusout(
            function(){

                $(this).css({opacity: "0.5"});
               $(".customized").animate({opacity: "0"});
            },

        );
    });





    jQuery('.toggle-comments-container').on('click', '.toggle-comments', function(e) {
    e.preventDefault();

    $(this).parent().next('.comment-content').fadeToggle('slow');

});





deletereply=function(replyid){


 $.ajax({
                    type: 'POST',
                    url: "../forum/reply/delete/"+replyid ,
                    data: {
                    'replyid':replyid,


                    'csrfmiddlewaretoken': csrftoken
                     },

                    success: function(response){
                    console.log(".reply"+replyid);
                $(".btnreplydelete").closest(".reply"+replyid).fadeToggle('slow');


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}
var replid;
var urlreply;
editreply=function(replyid, body){
$('#dialog').dialog('option', 'title', 'Edit Reply');
console.log(replyid);

$( "#dialog" ).css("display", "block");
$( "#dialog" ).dialog( "open" );
$( "#dialog" ).css("background-color", "black");
$( ".username" ).text(body);
$( "#body" ).val(body );
urlreply ="../forum/reply/edit/";
replid= replyid;
}

editcomment=function(replyid, body){
$('#dialog').dialog('option', 'title', 'Edit Comment');
console.log(replyid);
$( "#spanedit" ).text("");
$( "#dialog" ).css("display", "block");
$( "#dialog" ).css("background-color", "black");
$( "#dialog" ).dialog( "open" );

$( "#body" ).val(body);
urlreply ="../forum/comment/edit/";
replid= replyid;
}
editindb=function(){
bodyreply=$( "#body" ).val();
 $.ajax({
                    type: 'POST',
                    url:urlreply+replid ,
                    data: {
                    'replyid':replid,
                    'bodyreply':bodyreply,
                    'csrfmiddlewaretoken': csrftoken
                     },

                    success: function(response){
$('#dialog').dialog('close');
       var x = document.getElementById("snackbar");
      x.className = "show";

      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Edit completed sucessfully, The page will reload !");
  window.location.reload();
                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}



 deletecomment=function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../forum/comment/delete/"+id ,
                    data: {
                    'comment_id':id,


                    'csrfmiddlewaretoken': csrftoken
                     },

                    success: function(response){
                    console.log(".hello"+id);
$(".btncommentdelete").closest(".hello"+id).remove();
check();

                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}

 check= function(){
if ( $('.commentone').children().length == 0 ) {
    console.log("empty here");
    $(".comment-content").html('<div id="nocomments">\
    No comments yet\
        </div>');
}
}
check();



    var box  = document.getElementById('box');
var down = false;


 toggleNotifi=function(){
  if (down) {
    box.style.height  = '0px';
    box.style.opacity = 0;
    down = false;
  }else {
    box.style.height  = '510px';
    box.style.opacity = 1;
    down = true;
  }
}

});