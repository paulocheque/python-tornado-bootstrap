function randomPassword(length, chars) {
  var mask = '';
  if (chars.indexOf('a') > -1) mask += 'abcdefghijklmnopqrstuvwxyz';
  if (chars.indexOf('A') > -1) mask += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (chars.indexOf('#') > -1) mask += '0123456789';
  if (chars.indexOf('!') > -1) mask += '~`!@#$%^&*()_+-={}[]:";\'<>?,./|\\';
  var result = '';
  for (var i = length; i > 0; --i) result += mask[Math.round(Math.random() * (mask.length - 1))];
  return result;
}

if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function (str){
        return this.slice(-str.length) == str;
    };
}

if (typeof String.prototype.contains != 'function') {
    String.prototype.contains = function (str) {
        return this.indexOf(str) !== -1;
    };
}

function currentUrl() {
    return encodeURIComponent(window.location);
}

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      return pair[1];
    }
  }
  return null;
}

function small(text) {
  return "<small>" + text + "</small>";
}

function createLink(href, label) {
    var link = $("<a/>").attr("href", href).html(label);
    return link;
}

function createCheckbox(name, value) {
    var input = $("<input/>").attr("type", "checkbox").attr("name", name).attr("id", name);
    if (value == true || value == "true") {
        input.attr("checked", "checked");
    }
    return input;
}

function createImage(src, extraClass) {
    return '<img src="'+src+'" class="img-responsive admin-image '+(extraClass || "")+'"/>';
}

function createImages(srcs, extraClass) {
    var imgs = srcs.map(function(url) { return createImage(url, extraClass); })
    return imgs.join(" ");
}

// var columns = [];
// loadDataTable("{{ current_user.secret_key }}", "{{ current_user.id }}", "/api/", columns);
function loadDataTable(secretKey, userId, apiUrl, columns, amount, create, edit, del, htmlFields) {
  var defaultErrorHandler = function(response, status) {
      $.pnotify({
          type: 'notice',
          delay: 3000,
          title: 'Invalid action',
          text: 'Could not retrieve server data right now'
      });
  };

  var client = new SecretRestClient(secretKey, userId, apiUrl, "1");

  var secretTable = new SecretDataTable({
      table: $("#table-list"),
      formCreate: $("#form-create"),
      formEdit: $("#form-create"),
      columns: columns,
      create: create || true,
      edit: edit || true,
      del: del || true,
      htmlFields: htmlFields || [],
      onTableLoad: function(table) {
          client.list(0, amount || 500, function(lines, status) {
              for (var i in lines) {
                  var data = lines[i];
                  //console.debug(data);
                  table.createLine(data._id, data);
              }
          }, defaultErrorHandler);
      },
      onCreate: function(table, data) {
          var successHandler = function(response, status) {
              table.createLine(response._id, data);
          };
          client.create(data, successHandler, defaultErrorHandler);
      },
      onUpdate: function(table, id, data) {
          var successHandler = function(response, status) {
              var handler = function(response, status) {
                  table.updateLine(id, response);
              }
              client.read(id, handler);
          };
          client.update(id, data, successHandler, defaultErrorHandler);
      },
      onDelete: function(table, id, data) {
          var successHandler = function(response, status) {
              table.deleteLine(id, data);
          };
          client.del(id, successHandler, defaultErrorHandler);
      },
      onTableChange: function(table) {
      },
      onModalReady: function(modal) {
      }
  });
}