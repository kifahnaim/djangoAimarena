$("#file-input").change(function(e) {


  for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {

      var file = e.originalEvent.srcElement.files[i];

      var img = document.getElementById("blah");
      var reader = new FileReader();
      reader.onloadend = function() {
           img.src = reader.result;
      }
      reader.readAsDataURL(file);
      $("file-input").after(img);
  }

});




var file = document.getElementById('file-input');
file.onchange = function(e) {
var ext = this.value.match(/.([^.]+)$/)[1];
switch (ext) {
  case 'jpg':
  case 'bmp':
  case 'png':
  case 'tif':
  case 'gif':
   document.getElementById("submitimage").style["display"] = "inline-block";

    break;
  default:
    alert('Not allowed');
    this.value = '';
}
};



