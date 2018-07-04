var sendRequest = function (method, url, body) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            console.log(xhr);
            if (xhr.status === 200 || xhr.status === 0) {
                // on success
            } else {
                // on failure
            }
        }
    };
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(body));
};
