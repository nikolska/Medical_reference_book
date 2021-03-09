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
  $("#myInput3").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList3 li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#myInput4").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList4 li").filter(function() {
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


// Add new disease: if input is checked -> check selected option -> save id data object.
// const inputs = document.querySelectorAll("input.input-symptoms");
// const select_list = document.querySelectorAll("select.select-frequency");
// const results = [];
//
// function checkingSelect() {
//   for (let i=0; i<inputs.length; i++) {
//     if (inputs[i].checked) {
//       const data = `"symptom": "${inputs[i].value}","frequency": "${select_list[i].value}"`;
//       results.push(data);
//     }
//   }
// }
//
// checkingSelect();
// const json = { ...results };
//
// $.ajax(
//     {
//         url:'http://127.0.0.1:8000/diseases/add/',
//         data:json,
//         type:'post',
//         success:function(data){alert(data);},
//         error:function(){alert('error');}
//     }
// );
