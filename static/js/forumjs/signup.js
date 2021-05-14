	  var strong = false;
					function checkbutton(){

					if (strong){
 $("#create").removeAttr('disabled');


					}else {
$("#create").prop("disabled", true);


					}

					}


	function checkPasswordMatch() {
    var password = $("#password").val();
    var confirmPassword = $("#cpassword").val();

var x = $(".password-verdict").text();


if (x == 'Medium' || x == 'Strong' ||  x == 'Very Strong')
{
strong = true;
}else{
strong = false;
}
checkbutton();

if (password.length > 0 && confirmPassword.length > 0) {

    if (password != confirmPassword){
$("#pswdconfirm").text(String.fromCharCode(120) + ' - ' +'Passwords do not match');

        }
    else{

$("#pswdconfirm").text(String.fromCharCode(10003) + ' - ' +'Passwords match');
        }

        }
}

$("#password, #cpassword").keyup(checkPasswordMatch);



    "use strict";
    var options = {};
    options.ui = {
        bootstrap4: true,
        container: "#Pass",
        viewports: {
            progress: ".pwstrength_viewport_progress"
        },
        showVerdictsInsideProgressBar: true
    };
    options.common = {
        debug: true,
        onLoad: function () {


        }
    };
    $('#password').pwstrength(options);