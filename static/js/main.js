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
  $("#myInputTreatment").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#id_treatment li").filter(function() {
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

$(document).ready(function(){
  $("#myInput2").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable2 td").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
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

// allAreas = document.querySelector('#all_areas');
// allInputs = document.getElementsByName('geographical_area');
// console.log(allAreas);
// console.log(allInputs);

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
