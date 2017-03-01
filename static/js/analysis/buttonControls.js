/**
 * Created by dudegrim on 3/1/17.
 */

$(document).ready(function() {

  $('#first-level-c').on('toggle', function () {
      $("#second-level-c").attr('disabled', true);
      $('#second-level-c').radio("refresh");
  });
  $('#first-level-t').on('toggle', function () {
      // $("#third-level-t").attr('disabled', true);
      // $("#second-level-t").attr('disabled', true);
      // $('#third-level-t').radio("refresh");
      // $('#second-level-t').radio("refresh");
      $("#second-level-c").find("input").removeAttr("disabled");
      $('#second-level-c').radio("refresh");

  });
  $('#first-level-s').on('toggle', function () {
      $("#third-level-s").attr('disabled', true);
      $("#second-level-s").attr('disabled', true);
      $('#third-level-s').radio("refresh");
      $('#second-level-s').radio("refresh");
  });

  function candidates(){
        if($("#second-level-c").is(':enabled')) {
            $("#second-level-c").attr('disabled', true);
        }
        else{
            console.log("2c");
            // $("#second-level-c").attr('disabled', false);
        }
        $('#second-level-c').radio("refresh");

        if($("#third-level-c").is(':enabled')) {
            $("#third-level-c").attr('disabled', true);
        }
        else {
            console.log("3c");
            // $("#third-level-c").attr('disabled', false);
            $("#third-level-c").find("input").removeAttr("disabled");
        }
        $('#third-level-c').radio("refresh");
  }
});