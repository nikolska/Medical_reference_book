$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#myInputSymptom").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#id_symptoms li").filter(function() {
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

$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable td").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

const links = document.querySelectorAll("a.image");
const lightbox = document.querySelector(".lightbox");
const lightboxCtn = document.querySelector(".lightbox-cnt");
const img = document.querySelector(".lightbox-img");
const button = document.querySelector(".lightbox-close");

links.forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        img.src = link.href;
        lightbox.style.display = 'flex';
    })
});

button.addEventListener('click', e => {
    lightbox.style.display = 'none';
});

lightbox.addEventListener('click', e => {
    lightbox.style.display = 'none';
});

lightboxCtn.addEventListener('click', e => {
    e.stopPropagation();
});


$(document).ready(function(){
  $("input#id_image").on("change", function() {
    const imageFile = $("input#id_image").get(0).files[0];

    if (imageFile) {
      const reader = new FileReader();

      reader.onload = function () {
        $("#previewImg").attr("src", reader.result);
      };

      reader.readAsDataURL(imageFile);
    }
  })
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
//       console.log(data);
//     }
//   }
// }
//
// const obj = checkingSelect();
// $.ajax(
//     {
//         url:'http://127.0.0.1:8000/diseases/add/',
//         data:json,
//         type:'post',
//         success:function(data){alert(data);},
//         error:function(){alert('error');}
//     }
// );
