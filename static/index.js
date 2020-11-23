 // The loading function which makes the form disappear and making the loading message appear
 function loading() {
    $("#loading").show();
    $("#content").hide();
}
// On document being ready the loading message should be disabled 
$(document).ready(function () {
    $("#loading").hide();
});