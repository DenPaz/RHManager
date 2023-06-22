SetDatePicker();

$(document).ready(function () {
    const csrfToken = $('input[name=csrfmiddlewaretoken]')[0].value

    $('#file-upload').on('change', (e) => {
        $('#avatar-img')[0].src = URL.createObjectURL(e.target.files[0]);
    })

    const exportData = (type) => {

        const searchQuery = new URLSearchParams(location.search)

        $.ajax({
            url: '/transactions/export/',
            type: 'POST',
            data: {'type': type, 'search': searchQuery.get('search')},
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (result) {
                let a = document.createElement("a");
                a.href = `data:application/${result.file_format};base64,${result.content}`
                a.download = `data.${result.file_format}`
                a.click();
            },
            error: function () {
                notification.error('Error occurred');
            }

        });
    }

    $('#csv-export').click(() => {
        exportData('csv')
    })

    $('#pdf-export').click(() => {
        exportData('pdf')
    })

    // Delete Item
    $('.item-row').on('click', '.delete_item', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.data('href');
        var param = [];
        param['url'] = url;
        param['btn'] = btn;

        $.confirm({
                title: 'Warning!',
                content: 'Are you sure you want to delete?',
                type: 'red',
                buttons: {
                    yes: function () {
                        AjaxRemoveItem(param);
                    },
                    no: function () {
                    }
                }
            },
        );
    });

    // Edit Item by double click
    //$('.item-row').dblclick(function (event) {
    //    event.preventDefault();
    //    var item = $(this);
    //    var url = item.data('edit');
    //    var param = [];
    //    param['url'] = url;
    //    param['item'] = item;
    //    AjaxGetEditRowForm(param);
    //});

    // submit edit profile
    $('#form').on('submit', (e) => {

        const formData = new FormData($('#form')[0])

        const csrfToken = $('input[name=csrfmiddlewaretoken]')[0].value

        e.preventDefault()
        $.ajax({
            method: "POST",
            url: $('#form').attr('action'),
            processData: false,
            contentType: false,
            data: formData,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },

            success: function (data) {
                notification.success('edited successfully!')
            },

            failure: function (error) {
                notification.error('process has been fild!')
            }
        });

    });

    // Save form with click button
    $('.item-row').on('click', '.save_form', function (event) {
        event.preventDefault();
        var btn = $(this);
        SaveItem(btn);
    });

    // Save form with ENTER
    $('.item-row').keyup('.transaction', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            var btn = $(this);
            SaveItem(btn);
        }
    });

    // Cancel edit form
    $('.item-row').on('click', '.cancel_form', function (event) {
        event.preventDefault();
        var btn = $(this);
        var item = btn.closest('.item-row');
        var url = item.data('detail');
        var param = [];
        param['url'] = url;
        param['item'] = item;
        AjaxGetEditRowDetail(param);
    });
});


// Functions

function AjaxGetEditRowDetail(param) {
    $.ajax({
        url: param['url'],
        type: 'GET',
        success: function (data) {
            param['item'].html(data.edit_row);
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}

function AjaxGetEditRowForm(param) {
    $.ajax({
        url: param['url'],
        type: 'GET',
        success: function (data) {
            param['item'].html(data.edit_row);
            SetDatePicker();
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}

function AjaxPutEditRowForm(param) {
    $.ajax({
        url: param['url'],
        type: 'PUT',
        data: param['query'],
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            notification[data.valid](data.message);

            if (data.valid === 'success') {
                param['item'].html(data.edit_row);
                SetDatePicker();
            }
        },
        error: function () {
            toastr.error('Error occurred');
        }
    });
}

function AjaxRemoveItem(param) {
    $.ajax({
        url: param['url'],
        type: 'DELETE',
        data: param['query'],
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            if (data.valid !== 'success')
                notification[data.valid](data.message);

            if (data.valid === 'success') {
                if (data.redirect_url) {
                    window.location.replace(data.redirect_url);
                } else {
                    notification[data.valid](data.message);
                    var item_row = param['btn'].closest('.item-row');
                    item_row.hide('slow', function () {
                        item_row.remove();
                    });
                }
            }
        },
        error: function () {
            toastr.error('Error occurred');
        }
    });
}

function SaveItem(btn) {
    var item = btn.closest('.item-row');
    var url = item.data('edit');
    var param = [];
    param['url'] = url;
    param['item'] = item;
    param['query'] = $('.transaction').serialize();
    AjaxPutEditRowForm(param);
}

function SetDatePicker() {
    var datepickers = [].slice.call(d.querySelectorAll('.datepicker_input'));
    datepickers.map(function (el) {
        return new Datepicker(el, {format: 'yyyy-mm-dd'});
    });
}
