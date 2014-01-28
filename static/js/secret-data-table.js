/*
http://learn.jquery.com/plugins/basic-plugin-creation/

Example of Usage:

var secretTable = new SecretDataTable({
    table: $("#myTable"),
    columns: [
        function(data, id) { return linkify(data.description) },
        function(data, id) { return data.tags },
        function(data, id) {
            var button = $("<button/>");
            button.click(function() {
                // custom action
            });
            return button;
        },
    ],
    formCreate: $("#myForm"),
    formUpdate: $("#myForm"),
    create: true,
    edit: true,
    del: true,
    onTableLoad: function(table){},
    onCreate: function(table, data){ table.createLine(some_id, data); },
    onUpdate: function(table, id, data){ table.updateLine(id, data); },
    onDelete: function(table, id, data){ table.deleteLine(id, data); },
    onTableChange: function(table){},
    onModalReady: function(modal){}
});
*/
(function() {
    htmlEscape = function(text) {
        return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    };

    createModal = function(id, title, content) {
        var modal = $("<div/>").attr("id", "modal-" + id).attr("class", "modal fade");
        var divDialog = $("<div/>").attr("class", "modal-dialog");
        var divContent = $("<div/>").attr("class", "modal-content");
        var divHeader = $("<div/>").attr("class", "modal-header");
        var divBody = $("<div/>").attr("class", "modal-body");
        var divFooter = $("<div/>").attr("class", "modal-footer");
        divHeader.append($("<button/>").attr("type", "button").attr("class", "close").attr("aria-hidden", "true").attr("data-dismiss", "modal").html("&times;"));
        divHeader.append($("<h4/>").attr("class", "modal-title").html(title));
        if (content) {
            content.css("display", "block");
            divBody.append(content);
        }
        divFooter.append($("<button/>").attr("type", "button").attr("class", "btn btn-default").attr("data-dismiss", "modal").html("Close"));
        divContent.append(divHeader);
        divContent.append(divBody);
        divContent.append(divFooter);
        divDialog.append(divContent);
        modal.append(divDialog);
        modal.attr('tabindex', -1); // fix bootstrap keyboard ESC issue
        modal.on('hidden.bs.modal', function () {
            $(this).data('bs.modal', null);
            modal.remove();
        });
        modal.on('shown.bs.modal', function() {
            var firstInput = modal.find('input')[0]
            if (firstInput) firstInput.focus();
        });
        return modal;
    };

    var SecretDataTable = function(options) {
        this.settings = $.extend({
            table: null,
            columns: [],
            formCreate: $("<input/>"),
            formEdit: $("<input/>"),
            create: true,
            edit: true,
            del: true,
            onTableLoad: function(table){},
            onCreate: function(table, data){ table.createLine(data._id, data); },
            onUpdate: function(table, id, data){ table.updateLine(data); },
            onDelete: function(table, id, data){ table.deleteLine(data); },
            onTableChange: function(table){},
            onModalReady: function(modal){}
        }, options);

        var weakThis = this;

        this._createCreateButton = function() {
            var button = $("<button/>").attr("type", "button").attr("class", "btn btn-primary").html('<span class="glyphicon glyphicon-pencil"> New</span>');
            var onclick = function() {
                var form = weakThis.settings.formCreate.clone(false);
                form.on('submit', function (e) {
                    e.preventDefault();
                    if (weakThis.settings.onCreate) {
                        var formData = {};
                        $(this).serializeArray().map(function(x){ formData[x.name] = htmlEscape(x.value); });
                        weakThis.settings.onCreate(weakThis, formData);
                    }
                });

                var modal = createModal("new", "New record", form);
                modal.modal({});
                if (weakThis.settings.onModalReady) {
                    weakThis.settings.onModalReady(modal);
                }
            };
            button.click(onclick);
            return button;
        };

        this._createEditButton = function(id, data) {
            var button = $("<button/>").attr("type", "button").attr("class", "btn btn-default btn-xs").html('<span class="glyphicon glyphicon-edit"></span>');
            var onclick = function() {
                var form = weakThis.settings.formEdit.clone(false);
                for (var key in data) {
                    form.find("[name='" + key + "']").val(data[key]);
                }
                form.on('submit', function (e) {
                    e.preventDefault();
                    if (weakThis.settings.onUpdate) {
                        var formData = {};
                        $(this).serializeArray().map(function(x){ formData[x.name] = htmlEscape(x.value); });
                        weakThis.settings.onUpdate(weakThis, id, formData);
                    }
                });

                var modal = createModal(id, "Editing <small>" + id + "</small>", form);
                modal.modal({});
                if (weakThis.settings.onModalReady) {
                    weakThis.settings.onModalReady(modal);
                }
            };
            button.click(onclick);
            return button;
        };

        this._createDeleteForm = function(id, data) {
            var form = $("<form>").attr("method", "delete").attr("class", "form-delete");
            form.append('<button type="submit" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-trash"></span></button>');
            form.on('submit', function (e) {
                e.preventDefault();
                if (weakThis.settings.onDelete) {
                    weakThis.settings.onDelete(weakThis, id, data);
                }
            });
            return form;
        }

        this.createLine = function(id, data) {
            $("#modal-new").modal('hide');
            var newRow = $('<tr id="line-' + id + '">');
            for (var i in weakThis.settings.columns) {
                var text = weakThis.settings.columns[i](data, id);
                var col = $("<td>");
                col.append(text);
                newRow.append(col);
            }
            if (weakThis.settings.edit == true && weakThis.settings.formEdit) {
                var button = weakThis._createEditButton(id, data);
                var col = $("<td>");
                col.append(button);
                newRow.append(col);
            }
            if (weakThis.settings.del == true) {
                var form = weakThis._createDeleteForm(id, data);
                var col = $("<td>");
                col.append(form);
                newRow.append(col);
            }
            weakThis.settings.table.find("tbody:last").append(newRow);
            if (weakThis.settings.onTableChange) {
                weakThis.settings.onTableChange(weakThis);
            }
        }

        this.updateLine = function(id, data) {
            $("#modal-" + id).modal('hide');
            var line = weakThis.settings.table.find("#line-" + id);
            var columns = line.find("td");
            for (var i in weakThis.settings.columns) {
                var text = weakThis.settings.columns[i](data, id);
                var column = columns.eq(i);
                column.html(text);
                if (typeof column.effect === 'function') {
                    column.effect("highlight", {color:"#aaccff"}, 1000);
                } else {
                    column.fadeOut().fadeIn();
                }
            }
            if (weakThis.settings.onTableChange) {
                weakThis.settings.onTableChange(weakThis);
            }
        }

        this.deleteLine = function(id, data) {
            var line = weakThis.settings.table.find("#line-" + id);
            line.fadeOut().remove();
            if (weakThis.settings.onTableChange) {
                weakThis.settings.onTableChange(weakThis);
            }
        }

        if (weakThis.settings.create === true && weakThis.settings.formCreate) {
            var button = weakThis._createCreateButton();
            var newHead = $("<thead/>").append(button).append("<br/><br/>");
            weakThis.settings.table.prepend(newHead);
        }

        if (weakThis.settings.onTableLoad) {
            weakThis.settings.onTableLoad(weakThis);
        }

        return weakThis;
    };

    if(!window.SecretDataTable) { window.SecretDataTable = SecretDataTable };
    if(!window.htmlEscape) { window.htmlEscape = htmlEscape };
    if(!window.createModal) { window.createModal = createModal };

})();