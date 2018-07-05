// vim: ts=4 sts=4 sw=4

var sendRequest = function (method, url, body, span_id) {
    // TODO: set spinner icon on span id
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 0) {
                // TODO: on success set check icon
            } else {
                // TODO: on failure set error icon
                console.log(xhr);
            }
            // TODO: set timeout to clear span icon
        }
    };
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(body));
    return false;
};
