function checkinput (input){
console.log(input);
if (input.length > 0){

document.getElementById("send").disabled = false;
}else{

document.getElementById("send").disabled = true;
}
}
checkinput();

