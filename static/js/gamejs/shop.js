$( document ).ready(function() {
var productprice;
   showcheckoutmodal= function(id, name, price){
    productprice = price
    $('#exampleModal').modal('show');
        $("#productname").text(name);
        $("#productprice").text(price);
      $("#purchasebtn").val(id);

    }

   $('#purchasebtn').click(function() {
    console.log("clicked");
         id = $("#purchasebtn").val();
      $.ajax( {
           type :"POST",
            url:"../shop/purchase/"+id+"/",
             datatype :'json',
                data : {
                'product_id':id,
                'product_price':productprice,
                'csrfmiddlewaretoken': csrftoken,
              },


                success :function(response){
                    console.log(response["nopoints"]);
      var x = document.getElementById("snackbar");

     $(".pre-loader").css("display", "block");


      setTimeout(function(){
       $(".pre-loader").css("display", "none");
         x.className = "show";
       $("#snackbar").html(response["nopoints"]);
         $("#points").html(response["userpoints"]);
           $('#exampleModal').modal('hide');
        }, 3000);
      setTimeout(function(){ x.className = x.className.replace("show", "");  }, 4000);

                },
                error: function(rs, e){
                  console.log("oops error!");
                },

               });
 });

       });