$(document).ready(function(){
  var myForm = $('.signup-form');

  myForm.submit(function(event){
    event.preventDefault();
    $('.errors').empty();
    var formData = myForm.serialize();
    var formURL = myForm.attr('action');

    $.ajax({
      method: 'POST',
      url: formURL,
      data: formData,
      success: function(data){
        if (data.success){
          window.location.replace("http://localhost:8000/");
        } else {
          $.each(data.errors, function(index, item) {
            $(".errors").append(
              "<article class=\"message is-danger\">" +
                "<div class=\"message-body\">" +
                  item +
                "</div>" +
                "</article>"
            );
          })
        }
      },
    })
  });
});
