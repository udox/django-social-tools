(function($) {

    $(document).ready(function() {

        function setSelectOptions(data) {
            $('#tweet-msgs').html('<option></option>');
            for(var x=0; x<data.length; x++) {
                var msg = data[x].copy;
                var option = $('<option></option>').attr('value', msg).text(msg);
                $('#tweet-msgs').append(option);
            }
        }

        $('.send_tweet').on('click', function(e) {

            // This is a bit horrible but will grab the account text so we can get
            //the particular id for this to filter messages against
            var account = $(this).parent().parent().parent().prev().prev().prev().prev().text();
            var account_id = account.match(/\((\d+)\)/)[1];

            if($(this).data('msgtype') == 'tryagain') {
                $.getJSON('/api/messages/?type=f&account=' + account_id, setSelectOptions);
            } else {
                $.getJSON('/api/messages/?type=s&account=' + account_id, setSelectOptions);
            }

            $('#myModal').modal();
        });

        $('#tweet-msgs').on('change', function(e) {
            $('#tweet-msg').val($('#tweet-msgs').val());
        });

        $('.modal-tweet').on('click', function(e) {
            var target = 'jaymzcampbell';
            var msg = $('#tweet-msg').val();

            $(this).load('/send-tweet/?msg=' + escape(msg) + '&target=' + target);
        });

        var textareaPlaceholder = 'Add an internal note (not public)';
        $('#result_list .vLargeTextField').attr('placeholder', textareaPlaceholder);

    });

})(django.jQuery);
