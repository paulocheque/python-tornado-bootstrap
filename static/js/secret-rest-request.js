// RFC 2104 HMAC-SHA1
// HMAC-SHA256
// http://www.ietf.org/rfc/rfc2104.txt
// http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
// http://www.thebuzzmedia.com/designing-a-secure-rest-api-without-oauth-authentication/
// Dependencies:
// http://jquery.com
// https://code.google.com/p/crypto-js/#SHA-2
// https://code.google.com/p/crypto-js/#Encoders
// Example of Usage:
// var client = new SecretRestClient("private", "public", "/api/tasks", "1");
// client.list();
// client.read("111");
// client.create({data:"data1"});
// client.update("111", {data:"data1"});
// client.del("111");
// client.count();
(function() {
    var SecretRestClient = function(privateKey, publicKey, apiPrefix, apiVersion) {
        this.privateKey = privateKey;
        this.publicKey = publicKey;
        this.apiPrefix = apiPrefix;
        this.apiVersion = apiVersion || 1;

        this._hash = function(data) {
            var hash = CryptoJS.HmacSHA256(data, this.privateKey);
            // console.debug("SHA256 hash: " + hash);
            var hashInBase64 = CryptoJS.enc.Base64.stringify(hash);
            return hashInBase64;
        };

        this._getSignature = function(method, url, data) {
            if (!data) data = {};
            var dataPrepared = [];
            var keys = Object.keys(data).sort();
            for (var i in keys) {
                var key = keys[i];
                var value = data[key];
                // console.debug(key.toLowerCase() + "=" + value);
                dataPrepared.push(key.toLowerCase() + "=" + value);
            }
            dataPrepared = dataPrepared.join("&");
            var tokens = [method, url, dataPrepared];
            var string = tokens.join("__");
            var signature = this._hash(string);
            // console.debug("Data for signature: " + string);
            // console.debug("Signature: " + signature);
            return signature;
        };

        this._getRequestData = function(data, signature) {
            // console.debug("Data: " + data);
            // console.debug("Signature: " + signature);
            var authTimestamp = new Date().getTime();
            var authData = {
                auth_version: this.apiVersion,
                auth_public_key: this.publicKey,
                auth_timestamp: authTimestamp,
                auth_signature: signature
            };
            if (data) {
                return $.param(data) + "&" + $.param(authData);
            } else {
                return $.param(authData);
            }
        };

        this._request = function(method, url, data, success, error) {
            // console.debug(method);
            // console.debug(url);
            var signature = this._getSignature(method, url, data);
            var authenticatedData = this._getRequestData(data, signature);
            // console.debug("Data: " + data);
            // console.debug("Authenticated Data: " + authenticatedData);
            if (method == "DELETE") { // DELETE does not send params
                url = url + "?" + authenticatedData;
            }
            $.ajax({
                method: method,
                url: url,
                data: authenticatedData,
                beforeSend: function (xhr) { xhr.setRequestHeader("Authorization", "HMAC-SHA256 " + signature); }
            }).done($.proxy(success, this)).fail($.proxy(error, this));
        };

        this.list = function(initial, amount, success, error) {
            initial = initial || 0;
            amount = amount || 50;
            var data = {initial:initial, amount:amount};
            var method = "GET";
            var url = this.apiPrefix;
            this._request(method, url, data, success, error);
        };

        this.count = function(success, error) {
            var method = "GET";
            var url = this.apiPrefix + "/count";
            this._request(method, url, null, success, error);
        };

        this.create = function(data, success, error) {
            var method = "POST";
            var url = this.apiPrefix;
            this._request(method, url, data, success, error);
        };

        this.read = function(identifier, success, error) {
            var method = "GET";
            var url = this.apiPrefix + "/" + identifier;
            this._request(method, url, null, success, error);
        };

        this.update = function(identifier, data, success, error) {
            var method = "PUT";
            var url = this.apiPrefix + "/" + identifier;
            this._request(method, url, data, success, error);
        };

        this.del = function(identifier, success, error) {
            var method = "DELETE";
            var url = this.apiPrefix + "/" + identifier;
            this._request(method, url, null, success, error);
        };
    }
    if(!window.SecretRestClient) { window.SecretRestClient = SecretRestClient };
})();