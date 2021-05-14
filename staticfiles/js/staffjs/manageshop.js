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

  var productimage = $("#productimage");
var productsprite = $("#productsprite");
checknewproductimage = function(){
var productimage = document.getElementById('productimage');
var productsprite = document.getElementById('productsprite');
if (productimage.files.length !=0 && productsprite.files.length !=0){
 document.getElementById("submitproduct").style["display"] = "inline-block";
}else{
 document.getElementById("submitproduct").style["display"] = "none";

}


productimage.onchange = function(e) {
  var ext = this.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
    case 'gif':
    case 'jpeg':
    checknewproductimage();
      break;
    default:
      alert('Not allowed');
      this.value = '';
  }
};




productsprite.onchange = function(e) {
  var ext = this.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
    case 'gif':
    case 'jpeg':
checknewproductimage();

      break;
    default:
      alert('Not allowed');
      this.value = '';
  }
};


}
checknewproductimage();


var id;

         function edit(x,val,desc,price,type) {
id = x;
$('#dialog').dialog('option', 'title', 'Edit product');

     $( ".username" ).val(val);
          $( "#titleedit" ).val(val);
          $( "#descriptionedit" ).val(desc);
 $( "#priceedit" ).val(price);
 $( "#typeedit" ).val(type);
     $( "#dialog" ).css("display", "block");
      $( "#dialog" ).dialog( "open" );

         }
var file = document.getElementById('productimageedit');
var file2 = document.getElementById('productspriteedit');
console.log(file2.files.length);
function imagecheck(){
if (file.files.length != 0 && file2.files.length != 0 ){

  document.getElementById("submitedits").style["display"] = "inline-block";

}else{


}
}

     $(document).on('click', '#submitedits' , function(event){
    event.preventDefault();
    title=   $("#titleedit").val();
   desc = $("#descriptionedit").val();
   price =$("#priceedit").val();
   type =$("#typeedit").val();

        var formData = new FormData();
        formData.append("image1",file.files[0]);
        formData.append("image2",file2.files[0]);
        formData.append("title", title);
        formData.append("desc", desc);
        formData.append("price", price);
        formData.append("type", type);
        formData.append("product_id", id);

        $.ajax({
                        type: 'POST',
                        url: '../../staff/manageshop/editproduct/'+id+'/',

                        data : formData,
                        processData: false,
                        contentType: false,
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


       function deleteproduct (id){

             $.ajax({
                        type: 'POST',
                        url: '../../staff/manageshop/deleteproduct/'+id+'/',
                        data: {

                        'product_id' : id,
                        'csrfmiddlewaretoken': csrftoken,
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


 function undoproduct (id){

             $.ajax({
                        type: 'POST',
                        url: '../../staff/manageshop/undoproduct/'+id+'/',
                        data: {

                        'product_id' : id,
                        'csrfmiddlewaretoken': csrftoken,
                        },
                        dataType: 'json',
                        success: function(response){

                            console.log("success");
                            $( "#my_dialog" ).dialog( "close" );

                            _html= '<div class="alert alert-success"><strong>Success!</strong> Undo succesfully.</div>';
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

file.onchange = function(e) {
  var ext = this.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
    case 'gif':
    case 'jpeg':
    imagecheck();
      break;
    default:
      alert('Not allowed');
      this.value = '';
  }
};




file2.onchange = function(e) {
  var ext = this.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'jpg':
    case 'bmp':
    case 'png':
    case 'tif':
    case 'gif':
    case 'jpeg':
imagecheck();

      break;
    default:
      alert('Not allowed');
      this.value = '';
  }
};


imagecheck();


function onclickadd(){
var name = $("#title").val();
var desc = $('#description').val();
var price = $('#price').val();
var type = $('#type').val();
var formData = new FormData();
var productimage = document.getElementById("productimage");
var productsprite = document.getElementById("productsprite");
formData.append("productimage",productimage.files[0]);
formData.append("productsprite",productsprite.files[0]);
formData.append("name", name);
formData.append("desc", desc);
formData.append("price", price);
formData.append("type", type);
console.log(formData);


               $.ajax( {
                type :"POST",
                url:"{% url 'staff:createproduct'  %} ",
                data : formData,
                processData: false,
                contentType: false,
                success :function(response){
                window.location.reload();
                },
                error: function(rs, e){
                   console.log("oops error!");
                  },

                });

}


