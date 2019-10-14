$(document).ready(function(){
  var myForm = $('.form');

  myForm.submit(function(event){
    event.preventDefault();
    $('.info').empty();
    var formData = myForm.serialize();
    var formURL = myForm.attr('action');
    var path = window.location.pathname;

    $.ajax({
      method: 'POST',
      url: formURL,
      data: formData,
      success: function(data){
        if (data.success){
          if(path == '/feedback/') {
            myForm.each(function(){
                this.reset();
            });
            $(".info").append(
              "<article class=\"message is-success\">" +
                "<div class=\"message-body\">" +
                  data.message +
                "</div>" +
                "</article>"
            );
          } else if (path == '/signup/') {
            window.location.replace("http://localhost:8000/");
          } else {
            window.location.replace("http://localhost:8000/feedback/");
          }
        } else {
          $.each(data.errors, function(index, item) {
            $(".info").append(
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
