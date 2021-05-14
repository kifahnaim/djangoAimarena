$( document ).ready(function() {
    var file = document.getElementById('image');
    file.onchange = function(e) {
      var ext = this.value.match(/\.([^\.]+)$/)[1];
      switch (ext) {
        case 'jpg':
        case 'bmp':
        case 'png':
        case 'tif':
        case 'gif':
        console.log("accepted");
    
          break;
        default:
          alert('Not allowed');
          this.value = '';
      }
    };
    // Get the modal
    var modal = document.getElementById('id01');
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    
    
      $( function() {
        $( "#dialog" ).dialog({
          autoOpen: false,
          height: 500,
          width : 400,
    
          show: {
            effect: "size",
            duration: 500
          },
          hide: {
            effect: "size",
            duration: 500
          }
        });
    
    
      } );
    
      $( function() {
        $( "#dialogdelete" ).dialog({
          autoOpen: false,
          height: 270,
          width : 300,
    
          show: {
            effect: "size",
            duration: 500
          },
          hide: {
            effect: "size",
            duration: 500
          }
        });
    
    
      } );
    
    
    
    
    var mypostid,instancebutton;
       deletepost=function(id, val , body, instance){
      console.log(instance);
    mypostid = id;
    instancebutton = instance;
        $( "#dialogdelete" ).css("background-color", "black");
      $( "#dialogdelete" ).dialog( "open" );
      }
    
    
    $('.cancel').on("click", function(e){
            e.preventDefault();
         $( "#dialogdelete" ).dialog( "close" );
    });
        $('.link-deletepost').on("click", function(e){
            e.preventDefault();
            var token =csrftoken;
    
            var $this = $('.link-delete goback');
            console.log($this);
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: '../../forum/my_posts/delete/'+mypostid+'/',
                type: "POST",
                dataType: "json",
                success: function(resp){
                    if(resp.message == 'success'){
                      $( "#dialogdelete" ).dialog( "close" );
                                console.log("success");
                        $(instancebutton).parents('.table-row').remove();
                              var x = document.getElementById("snackbar");
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
          $("#snackbar").html("Post deleted successfully !");
    
                    }
                    else{
                    alert(resp.message);
                    }
    
                },
                error: function(resp){
                console.log("Something went wrong");
                }
            });
    
    
    
        });
    
    
    
    
            $('#submiteditpost').on("click", function(e){
            var file = document.getElementById('image');
            e.preventDefault();
                   title = $("#title").val();
            body = $("#body").val();
            var formData = new FormData();
            formData.append("image",file.files[0]);
            formData.append("title", title);
            formData.append("body", body);
            console.log(formData);
    
            var token = '{{csrf_token}}';
            e.preventDefault();
            var $this = $(this).val();
            console.log($("#editurl").attr("href"));
            $.ajax({
    
                    url:'../../forum/my_posts/edit/'+$this+'/',
                    type: "POST",
                    data : formData,
                    processData: false,
                    contentType: false,
                    dataType: "html",
      success: function(resp){
    
     $( "#dialog" ).dialog( "close" );
     $(".container").html(resp);
    
          var x = document.getElementById("snackbar");
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
          $("#snackbar").html("Post edited successfully !");
    
                },
                error: function(resp){
                console.log("Something went wrong");
                }
            });
    
        });
    
    
    
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