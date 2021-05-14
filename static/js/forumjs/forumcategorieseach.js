

$( document ).ready(function() {
pinpost= function(id){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/pin/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },

                    success: function(response){
      var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Post pinned successfully !");


                       setTimeout(function() {
                                   $('#success').fadeOut();
                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}

unpinpost= function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/unpin/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },

                    success: function(response){
                                                        var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Pin removed successfully !");


                       setTimeout(function() {

                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}





acceptpost = function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/accept/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },


                    success: function(response){
                                                        var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Post accepted !");


                       setTimeout(function() {

                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}





rejectpost = function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/reject/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },

                    success: function(response){
                                                        var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Post rejected !");


                       setTimeout(function() {

                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}





acceptappeal= function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/acceptappeal/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },

                    success: function(response){
                                                        var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Appeal accepted !");


                       setTimeout(function() {

                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}




rejectappeal = function(id, val){
console.log(id);

 $.ajax({
                    type: 'POST',
                    url: "../../forum/rejectappeal/"+id ,
                    data: {
                    'post_id':id,
                    'csrfmiddlewaretoken': csrftokrn
                     },

                    success: function(response){
                                                        var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      $("#snackbar").html("Appeal rejected !");


                       setTimeout(function() {

                                    window.location.href =''
                               }, 2000);


                    },

                    error: function(rs, e){

                        console.log("error");
                    },
            });


}

var box  = document.getElementById('box');
var down = false;

toggleNotifi = function(){
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


$("#showimage").click(function() {

$(".drag-area").fadeToggle(500);

});

});