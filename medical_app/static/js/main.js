$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

// let checked = document.querySelectorAll('#symptoms');
// let values = [];
// for (let i = 0; i < checked.length; i++) {
//     if (checked[i].checked) {
//          let selectId = checked[i].getAttribute("data-select");
//          let resultValue = document.getElementById(selectId).value;
//          values.push(resultValue);
//     }
// }
