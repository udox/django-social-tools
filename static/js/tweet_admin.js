(function($) {

    $(document).ready(function() {

        $('.send_tweet').on('click', function(e) {
            $('#myModal').modal();
        });

        $('.modal-tweet').on('click', function(e) {
            $(this).load('/send-tweet/');
        });

    });

})(django.jQuery);
