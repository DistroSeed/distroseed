$( "#buttonselectnoencryption" ).click(function() {
  $("#buttonselectnoencryption").attr("class", "btn btn-default active");
  $("#buttonselectpreferredencryption").attr("class", "btn btn-default");
  $("#buttonselectrequiredencryption").attr("class", "btn btn-default");
});

$( "#buttonselectpreferredencryption" ).click(function() {
  $("#buttonselectnoencryption").attr("class", "btn btn-default");
  $("#buttonselectpreferredencryption").attr("class", "btn btn-default active");
  $("#buttonselectrequiredencryption").attr("class", "btn btn-default");
});

$( "#buttonselectrequiredencryption" ).click(function() {
  $("#buttonselectnoencryption").attr("class", "btn btn-default");
  $("#buttonselectpreferredencryption").attr("class", "btn btn-default");
  $("#buttonselectrequiredencryption").attr("class", "btn btn-default active");
});
