$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#myInput2").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList2 li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#searchInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#searchList li").each( function() {
      let text = $(this).attr('data-name').toLowerCase();
      if (text.includes(value)) {
        $(this).show();
      } else {
        $(this).hide();
      }
    })
  });
});

/*
Add new disease: if input is checked -> check selected option -> save id data object.

const inputs = document.querySelectorAll("input.input-class-s");
const select_list = document.querySelectorAll("select.select-s");

function checkingSelect() {
  for (let i=0; i<inputs.length; i++) {
    if (inputs[i].checked) {
      const input = inputs[i].value;
      const select = select_list[i].value;
      const data = {'symptom': input,
        'frequency': select};
      console.log(data);
      return data;
    }
  }
}

checkingSelect();
*/
