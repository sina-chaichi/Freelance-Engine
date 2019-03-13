login ={
init: function(){
  function send_login(){
    $.ajax({
        url : '/users/login/',
        type : 'POST',
        data : {
          password : $('#pass').val(),
          email : $('#email').val(),
          csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
       },

     }).done(function(data){
         if (data.status == false){
           $('#message-div').html(data.message);
           $('#pass').val('');
         }else{
           window.location.replace("http://127.0.0.1:8000");
         }
     });
  }

  $('#signin').on('click', function(event){
    event.preventDefault();
    send_login();
});

}
}
