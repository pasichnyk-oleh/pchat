$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    if (typeof socket_url !== "undefined") {
        updater.start();
    }

    $("form button.main_handler").click(function() {
        form = $(this).parent('form');
        url = form.attr('action');
        result_selector = $(this).attr('data-result-selector');

        data = get_form_data(form);

        request_and_insert(url, 'POST', data, result_selector, 'OMG! HACKED!');

        cleam_form_fields(form);
    });

    $("form button.socket_handler").click(function() {
        form = $(this).parent('form');
        data = get_form_data(form);

        updater.socket.send(JSON.stringify(data));

        cleam_form_fields(form, 'input:visible')
    });

    $(document).on('click', '.join', function() {
        url = $(this).attr('data-url');

        request_and_insert(url, 'GET', [], '.chats_block')
    });
});

function cleam_form_fields(form, fields) {
    //cleaning form fields
    if (!form.is('[data-clean-fields]')) {
        return
    }

    form.find(fields || 'input').each(function() {
        $(this).val('');
    });
}

function get_form_data(form, selectors_to_find) {
    data = {};

    form.find(selectors_to_find || 'input').each(function() {
        data[$(this).attr('name')] = $(this).val();
    });

    return data
}

function request_and_insert(url, method, data, insert_selector, error) {
    $.ajax({
        type: method,
        url: url,
        data: data
    }).done(function(html) {
        $(insert_selector).html(html);
    }).fail(function() {
        alert(error || "Sorry, try later!");
    })
}

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + socket_url;

        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        };
    },

    showMessage: function(data) {
        var existing = $("#message-" + data.id);

        if (existing.length > 0) {
            return;
        }

        $(".messages_block").prepend(data.message);
    }
};