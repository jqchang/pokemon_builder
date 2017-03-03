$(document).ready(function() {
  $("#result").click(function() {
    result = $.ajax({
      url: "/teambuilder/battle_ajax",
      success: function(obj) {
        $("#winner").text(obj.winner + " wins!");
        $('#result').hide();
      }
    });
  });
});
