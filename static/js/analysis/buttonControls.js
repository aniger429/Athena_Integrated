$(document).ready(function() {
      $('.first-level').on('toggle', function () {
          $(".second-level").attr('disabled', false);
          $(".third-level").attr('disabled', false);
          $('.second-level-label').removeClass('disabled');
          $('.third-level-label').removeClass('disabled');

          if($("#first-level-c").is(':checked')) {
            $("#second-level-c").attr('disabled', true);
            $("#third-level-c").attr('disabled', true);
            $('.second-level-label').removeClass('enabled');
            $('.third-level-label').removeClass('enabled');
          }
          if($("#first-level-t").is(':checked')) {
            $("#second-level-t").attr('disabled', true);
            $("#third-level-t").attr('disabled', true);
            $('.second-level-label').removeClass('enabled');
            $('.third-level-label').removeClass('enabled');
          }
          if($("#first-level-s").is(':checked')) {
            $("#second-level-s").attr('disabled', true);
            $("#third-level-s").attr('disabled', true);
            $('.second-level-label').removeClass('enabled');
            $('.third-level-label').removeClass('enabled');
          }

          $('.second-level').checkbox("refresh");
          $('.third-level').checkbox("refresh");
      });
// {#       $('.second-level').on('toggle', function () {#}
// {#               $('.third-level').each(function() {#}
// {#                   if($(this).is(':enabled')) {#}
// {#                    $('.third-level-label').removeClass('disabled');#}
// {#                    $('.third-level').attr('disabled', false);#}
// {##}
// {#                   }#}
// {#              });#}
// {##}
// {#               if($("#first-level-t").is(':enabled')) {#}
// {#                $("#second-level-t").attr('disabled', true);#}
// {#                $("#third-level-t").attr('disabled', true);#}
// {#                $('.third-level-label').removeClass('enabled');#}
// {#              }#}
// {#              $('.third-level').checkbox("refresh");#}
// {#      });#}

    });