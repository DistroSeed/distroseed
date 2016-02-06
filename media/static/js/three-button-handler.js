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

$( "#transmissionlogginglevelbuttonnone" ).click(function() {
  $("#transmissionlogginglevelbuttonnone").attr("class", "btn btn-default active");
  $("#transmissionlogginglevelbuttonerror").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttoninfo").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttondebug").attr("class", "btn btn-default");
});

$( "#transmissionlogginglevelbuttonerror" ).click(function() {
  $("#transmissionlogginglevelbuttonnone").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttonerror").attr("class", "btn btn-default active");
  $("#transmissionlogginglevelbuttoninfo").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttondebug").attr("class", "btn btn-default");
});

$( "#transmissionlogginglevelbuttoninfo" ).click(function() {
  $("#transmissionlogginglevelbuttonnone").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttonerror").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttoninfo").attr("class", "btn btn-default active");
  $("#transmissionlogginglevelbuttondebug").attr("class", "btn btn-default");
});

$( "#transmissionlogginglevelbuttondebug" ).click(function() {
  $("#transmissionlogginglevelbuttonnone").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttonerror").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttoninfo").attr("class", "btn btn-default");
  $("#transmissionlogginglevelbuttondebug").attr("class", "btn btn-default active");
});
