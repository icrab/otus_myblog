$(document).ready(function() {
   let newDiv = '<div class="alert alert-success" role="alert">'+
             '<h4 class="alert-heading text-center">Для просмотра содержимого сайта необходимо авторизоваться</h4>'+
             '</div>';
   $('.container').after(newDiv);
   $('.auth').click();
})