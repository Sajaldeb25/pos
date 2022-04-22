function ajaxRequest(data, functionName, url=window.location.href, type='POST') {
    $.ajax({
        url: url,
        type: type,
        data: data,
        success: function (data, textStatus, jqXHR) {
            window[functionName + 'Success'](data, textStatus, jqXHR)
        },
        error: function (data, textStatus, jqXHR) {
            window[functionName + 'Error'](data, textStatus, jqXHR)
        }
    });
}