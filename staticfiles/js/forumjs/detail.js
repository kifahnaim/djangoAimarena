$( document ).ready(function() {

var box  = document.getElementById('box');
var down = false;


 toggleNotifi= function(){
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


clearall = function(){

 $.ajax({

                url:'../../forum/clearall',
                type: "POST",
                data :
                {

                },
                dataType: "json",
  success: function(resp){
$(".notifi-item").hide();
$("#countnot").html("0");
toggleNotifi();
            },
            error: function(resp){
            console.log("Something went wrong");
            }
        });

}


readnotification= function(id, notid, sender, user){

 $.ajax({

                url:'../../forum/my_posts/read/'+id+'/',
                type: "POST",
                data :
                {
                "postid": id,
                "notid": notid,
                "sender":sender,
                "user" : user,

                },
                dataType: "json",
  success: function(resp){
    $("#clickread").closest('.notifi-item').remove();
     console.log($("#count1").text());
    x= parseInt($("#count1").text()) - parseInt(1);
    console.log(x);

 $(location).attr('href', '../../forum/'+id)



    $("#count1").html( x );
    $("#count2").html( x);
            },
            error: function(resp){
            console.log("Something went wrong");
            }
        });

}

    openmodal= function(id){
        console.log(id);


$.ajax({
                        type: 'POST',
                        url:'../../staff/users/'+id+'/',
                        data: {

                         'id':id,
                        'csrfmiddlewaretoken': csrftoken
                        },

                        success: function(response){
                                console.log(response.data);

                                $("#usernameuserprofile").text("@ " +response.data[0].Username);
                                $("#userroleuserprofile").text(response.data[0].Role_id__RoleName);
                           $('#userimageuserprofile').attr('src','/media/'+response.data[0].user_thumbnail );
                           $('#userimageuserprofile2').attr('src','/media/'+response.data[0].user_thumbnail );
                console.log(response.data.length);
                $("#postnumbers").text(response.data.length);
$("#fullnameuserprofile").text(response.data[0].Firstname +" "+ response.data[0].Lastname);
                        $(".containerprofile").show();


                        },
                        error: function(rs, e){

                            console.log("error");
                        },
                });


    }

$("#close").click(function(){
$(".containerprofile").hide();
});



});