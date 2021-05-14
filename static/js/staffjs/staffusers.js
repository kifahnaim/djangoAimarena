document.addEventListener("DOMContentLoaded", function(event) {
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

     openbootstrapmodal=function(id){

    console.log(id);
var userprofileurl =$("#userprofileurl").attr('href');
console.log(userprofileurl);
$.ajax({
                        type: 'POST',
                        url:'../../staff/users/'+id+'/',
                        data: {

                         'id':id,
                        'csrfmiddlewaretoken': csrftoken
                        },

                        success: function(response){
                                console.log(response.data);

                                $("#usernameuserprofile").text(response.data[0].Username);
                                $("#userroleuserprofile").text(response.data[0].Role_id__RoleName);
                           $('#userimageuserprofile').attr('src','/media/'+response.data[0].user_thumbnail );

$("#fullnameuserprofile").text(response.data[0].Firstname +" "+ response.data[0].Lastname);
                            $('#modalbootstrap').click();


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
    }
var bangameid;
                         dialogfunc=function(x,val) {
                         bangameid= val;
$('#dialog').dialog('option', 'title', 'Ban from forum');
$("#roles").css("display", "none");
        console.log(val);
        $('#dialog').dialog('widget').attr('id', 'forum');

$("#text").css("display", "block");
       $ ("#dtext").text("Banning the user will remove his privileges from accessing into the forum ");
         $ ("#first").text("Are you sure you want to ban " + x + " from forum ");
     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );
    console.log($("#dialog").attr('id'));
$("#ban").val(val);
  }


            dialogfuncgame=function(x,val) {
                   $('#dialog').dialog('widget').attr('id', 'game');
bangameid= val;
    $('#dialog').dialog('option', 'title', 'Ban from game');
        console.log(val);
        $("#roles").css("display", "none");
        $("#text").css("display", "block");
      $ ("#dtext").text("Banning the user from game will stop his privileges from playing ");
         $ ("#first").text("Are you sure you want to ban "+ x +" from game" );

     $( "#dialog" ).css("display", "block");
      $("#ban").val(val);
      $( "#dialog" ).dialog( "open" );
     console.log($("#dialog").attr('id'));

  }
var rankingid;
  dialogranking=function(x,val) {
rankingid = val;
$('#dialog').dialog('option', 'title', 'Ranking');
        console.log(val);
         $ ("#dtext").text("Ranking is promoting and demoting users according to their behaviour and loyalty ");
         $ ("#first").text("Are you sure you want to change the rank of "+ x);
$("#ban").html("Save changes");
$('#ban').attr('id','savechanges');

        $("#text").css("display", "none");
        $("#roles").css("display", "block");
     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );




  }


                $(document).on('click', '#ban' , function(event){
                event.preventDefault();

        var banurl= $("#banurl").attr('href');
         var pk = $(this).attr('value');

         var hours = $("#hours").val();
            console.log(hours);

            var title = $( "#dialog" ).dialog( "option", "title" );
            console.log(title);
        $.ajax({
                        type: 'POST',
                        url: banurl,
                        data: {
                        'choice': title,
                        'hours':hours  ,
                        'user_id' : bangameid,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){
                            console.log("worked");
                            console.log(pk);

                            console.log("success");
                            $('#dialog').dialog('close');
                            _html= '<div class="alert alert-success"><strong>Success!</strong> Banned succesfully.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                   window.location.reload();
                               }, 5000);

                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
            });




              $(document).on('click', '#kickbtn' , function(event){
                event.preventDefault();

        var kickurl= $("#kickurl").attr('href');
         var pk = $(this).attr('value');
        $.ajax({
                        type: 'POST',
                        url: '../../staff/kick/'+pk+'/',
                        data: {
                        'user_id' : pk,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){
                            console.log("worked");
                            console.log(pk);
          _html= '<div class="alert alert-success"><strong>Success!</strong> Kicked succesfully. This page will reload to save your changes.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                    window.location.reload();
                               }, 3000);


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
            });


                $(document).on('click', '#unbanbtn,#unban' , function(event){
                event.preventDefault();
                  var unbanurl= $(".unbanurlgame").attr('href');
                  var choice = jQuery(this).attr("id");
                  var pk = $(this).attr('value');
                   console.log("unban clicked");
                $.ajax({
                        type: 'POST',
                        url: unbanurl,
                        data: {
                        'choice': choice,
                        'user_id' : pk,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){


                            console.log("success");
                            $('#dialog').dialog('close');
                            _html= '<div class="alert alert-success"><strong>Success!</strong> Ban removed succesfully. This page will reload to save your changes. </div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                   window.location.reload();
                               }, 3000);

                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });

                });
    var role=1;
  $("#roles").change(function(){
         role = $(this).children("option:selected").val();
          console.log(role);
    });

   $(document).on('click', '#savechanges' , function(event){

    var rankingurl =$("#rankingurl").attr('href');

           var updaterankurl= $("#kickurl").attr('href');
         var pk = $("#Ranking").attr('value');
         console.log(pk);
                event.preventDefault();
                console.log("clicked");
                console.log('../../staff/users/updaterank/'+rankingid+'/');
 $.ajax({
                        type: 'POST',
                        url: '../../staff/users/updaterank/'+pk+'/',
                        data: {
                        'role': role,
                        'user_id' : rankingid,
                        'csrfmiddlewaretoken': csrftoken
                        },
                        dataType: 'json',
                        success: function(response){


                            console.log("success");
                            $('#dialog').dialog('close');
                            _html= '<div class="alert alert-success"><strong>Success!</strong> Rank updated successfully.</div>';
                             $("#success").append(_html);

                               setTimeout(function() {
                                   $('#success').fadeOut();
                                window.location.reload();
                               }, 3000);

                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });
                });


});