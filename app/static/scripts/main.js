var emojies = [];
$( ".emoji-card" ).click(function() {
   var elem = $(this);
   elem.toggleClass( "emoji-card-focus", !elem[0].classList.contains("emoji-card-focus"));
   if (elem[0].classList.contains("emoji-card-focus")) {
       if ($.inArray(elem[0].id, emojies) == -1) {
           emojies.push(elem[0].id);
       }
   }
});
$("#post-button").click(function () {
  $.get( "/search", {string: emojies.toString()}, function (data) {
      $( ".result" ).html(data);
  });
});