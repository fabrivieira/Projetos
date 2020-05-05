function postAjax(url, form, data) {
    
    
    var formData = new FormData(form);

    for (x in data) {
        formData.append(x, data[x]);
    }

    return $.ajax({
        type: "POST",
        url: url,
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    });
    
}
