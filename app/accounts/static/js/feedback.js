$(document).ready(function(){
  var myForm = $('.feedback-form');

  myForm.submit(function(event){
    event.preventDefault();
    $('.info').empty();
    var formData = myForm.serialize();
    var formURL = myForm.attr('action');

    $.ajax({
      method: 'POST',
      url: formURL,
      data: formData,
      success: function(data){
        if (data.success){
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
