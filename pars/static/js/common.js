// jQuery tabs

$(function() {
  $( ".tabs" ).tabs({
    beforeLoad: function( event, ui ) {
      ui.jqXHR.fail(function() {
        ui.panel.html(
          "Couldn't load this tab." );
      });
    }
  });
});

$(function() {
  $( "input[type=button]" )
    .button()
    .click(function( event ) {
      event.preventDefault();
    });
});
$(function() {
  $( ".accordion" ).accordion({
    collapsible: true,
    active: false,
    event: "click"
  });
});

$("p").each(function() {
  $(this).html($(this).html().replace(/nextlineAK/g,"<br>"));
});