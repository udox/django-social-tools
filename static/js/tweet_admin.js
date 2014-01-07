(function($) {

    $(document).ready(function() {

        $('.send_tweet').on('click', function(e) {

            if($(this).data('msgtype') == 'tryagain') {
                $('#tweet-msg').html("Please try again!");
            } else {
                $('#tweet-msg').html("Check this out! <PHOTOSHOP LINK>");
            }

            $('#myModal').modal();
        });

        $('.modal-tweet').on('click', function(e) {
            var target = 'jaymzcampbell';
            var msg = 'TBC';

            $(this).load('/send-tweet/?msg=' + msg + '&target=' + target);
        });

    });

})(django.jQuery);
