(function($) {
    $.fn.asyncForm = function(success, error) {
        return $(this).on('submit', function (e) {
            $.ajax({
                url: $(this).attr('action') || $(this).attr('target'),
                method: $(this).attr('method') || 'POST',
                data: $(this).serialize()
            }).done($.proxy(success, this)).fail($.proxy(error, this));

            e.preventDefault();
        });
    };
})(jQuery);

(function($) {
    $.fn.populateTable = function(success, error) {
        var initial = $(this).attr('initial') || 0;
        var amount = $(this).attr('amount') || 50;
        $.ajax({
            url: $(this).attr('action') || $(this).attr('target'),
            method: $(this).attr('method') || 'GET',
            data: "initial=" + initial + "&amount=" + amount
        }).done($.proxy(success, this)).fail($.proxy(error, this));
    };
})(jQuery);

function addTableLine(tableId, cols) {
    var newRow = $("<tr>");
    for (var i in cols) {
        var text = cols[i];
        var col = $("<td>");
        col.append(text);
        newRow.append(col);
    }
    $("#" + tableId).find("tbody:last").after(newRow);
}

function createUpdateForm(url) {
    var form = $("<form>").attr("action", url).attr("method", "put").attr("class", "form-update");
    form.append('<button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-edit"></span></button>');
    form.asyncForm(function(data, status) {
    }, function(data, status) {
        $.pnotify({
            type: 'notice',
            delay: 3000,
            title: 'Invalid action',
            text: 'Please, fix your data and try again'
        });
    });
    return form;
}

function createDeleteForm(url) {
    var form = $("<form>").attr("action", url).attr("method", "delete").attr("class", "form-delete");
    form.append('<button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-trash"></span></button>');
    form.asyncForm(function(data, status) {
        $(this).closest("tr").remove();
    }, function(data, status) {
        $.pnotify({
            type: 'notice',
            delay: 3000,
            title: 'Invalid action',
            text: 'Could not delete this item'
        });
    });
    return form;
}

function createEditableField(name, value) {
    var fixed = $("span").html(value);
    var editable = $("input").attr("type", "text").attr("class", "").attr("name", name).attr("value", value);
    return $("div").append(fixed).append(editable);
}