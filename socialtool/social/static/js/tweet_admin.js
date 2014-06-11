window.reloader = null;

(function($) {

    $(document).ready(function() {

        var TIMEOUT_DELAY = 30;  // seconds
        var post_pk;
        var handle;
        var started = new Date().getTime();

        function setSelectOptions(data) {
            $('#tweet-msgs').html('<option></option>');
            for(var x=0; x<data.length; x++) {
                var msg = data[x].copy;
                var option = $('<option></option>').attr('value', msg).text(msg);
                $('#tweet-msgs').append(option);
            }
        }

        function pageReloader() {
            console.log("Starting page reload request");
            $('#load-overlay').fadeIn();
            $('div#changelist').load(window.location.href + ' div#changelist', setupPage);
        }

        function setupPage() {
            $('#load-overlay').fadeOut();
            console.log("Setting up page", new Date().getTime() - started);

            setupHandlers();
            initElements();
            clearTimeout(window.reloader);
            window.reloader = window.setTimeout(pageReloader, TIMEOUT_DELAY * 1000);
        }

        function checkTweetLength() {
            var length = $('#tweet-msg').val().length;
            if(length > 140) {
                $('#tweet-msg').css({'background-color': '#fcc'});
            } else {
                $('#tweet-msg').css({'background-color': '#cfc'});
            }
            $('#tweet-length').html('Length: ' + length);
        }

        function get_post_pk(elem) {
            return $(elem).closest('td').prevAll(':last').find('.action-select').val();
        }

        function setupHandlers() {
            console.log("Setting up handlers");

            $('.send-tweet').on('click', function(e) {

                // This is a bit horrible but will grab the account text so we can get
                //the particular id for this to filter messages against
                var account = $(this).parent().parent().parent().prev().prev().prev().prev().prev().text();
                var account_id = account.match(/\((\d+)\)/)[1];
                post_pk = get_post_pk(this);
                handle = $(this).closest('td').prevAll(':eq(5)').find('a').text();

                // reset modal form
                $('#tweet-msg').val('');
                $('#tweet-log').html('');
                $('.modal-tweet').val('Send').show();

                // TODO: you should be ashamed! pass as obj instead and undupe this!
                if($(this).data('msgtype') == 'tryagain') {
                    $.getJSON('/api/messages/?type=f&account=' + account_id, setSelectOptions);
                } else {
                    $.getJSON('/api/messages/?type=s&account=' + account_id, setSelectOptions);
                }

                $('#myModal').modal();
            });

            $('#tweet-msg').on('keyup', checkTweetLength);

            $('#tweet-msgs').on('change', function(e) {
                $('#tweet-msg').val('@' + handle + ' ' + $('#tweet-msgs').val());
                checkTweetLength();
            });

            $('.modal-tweet').on('click', function(e) {
                var msg = $('#tweet-msg').val();
                $(this).fadeOut();
                $(this).prev('a').text('Close');
                $(this).parentsUntil('#modal').find('#tweet-log').load('/send-tweet/?msg=' + encodeURIComponent(msg) + '&post_pk=' + post_pk);
            });

            // Inprogress notification
            $('.assign-artworker').on('click', function(e) {
                $(this).load('/assign-artworker/?post_pk=' + get_post_pk(this));
            });

            // Hellban
            $('.ban-user').on('click', function(e) {
                $(this).load('/ban-user/?post_pk=' + get_post_pk(this));
            });

        }

        function initElements() {
            console.log("Initializing elements and page layout");

            // Notes placeholders
            var textareaPlaceholder = 'Add an internal note (not public). Remember to click save!';
            $('#result_list .vLargeTextField').attr('placeholder', textareaPlaceholder);

            // Set background color if item has been tweeted
            $('tbody tr').each(function() {

                if($('td:eq(9)', this).text() !== '(None)') {
                    $('td, th', this).css({'background': '#fef'});
                } else {
                    $('td, th', this).css({'background': '#eff'});
                }

            });
        }

        setupPage();

    });

})(django.jQuery);
