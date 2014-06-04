API Authentication
------------------

An API key is required to access the Takoman API. A user account is not, unless you want to perform actions on behalf of the user.

There're three ways to authenticate to the Takoman API:

* Using an XAPP Token obtained using a client application ID and secret without logging in.
* Logging in using an XAuth Token obtained using a client application ID, secret and a user's email and password.
* Logging in using an XAuth Token obtained from a user's OAuth Token, usually on a mobile device.

### Get an Application Key
TODO

### Authenticate with an XAPP Token

This workflow is suitable for desktop or mobile clients. It allows anonymous logon to Takoman without any user access.

```
http://localhost:5000/api/v1/xapp_token
    ?client_id=[your client id]
    &client_secret=[your client secret]
```

The response from Takoman will be the following JSON.

```bash
{ xapp_token" : [xapp token], "expires_in" : [expiration time] }
```

Make requests by placing the token into an "X-Xapp-Token" header. Here's a complete example.

```bash
$ curl "http://localhost:5000/api/v1/xapp_token?client_id=...&client_secret=..."
{ "xapp_token" : "JvTPWe4WsQO ... g4lGBrISMwnjGT8", "expires_in" : "2013-08-28T12:10:22Z" }

$ curl -H "X-XAPP-TOKEN:JvTPWe4WsQO ... g4lGBrISMwnjGT8" "http://localhost:5000/api/v1/users"
[{"name": "Tako Man", ...}]
```

### Login using an XAuth Token obtained from a User's Email and Password

If you store user's email and password, you can obtain an OAuth token in exchange for those credentials.

```
http://localhost:5000/oauth2/access_token
    ?client_id=[your client id]
    &client_secret=[your client secret]
    &grant_type=credentials
    &email=[user's e-mail]
    &password=[user's password]
```

The response from Takoman will be the following JSON.

```bash
{ "access_token" : [access token], "expires_in" : [expiration time] }
```

Make requests by placing the token into an "X-Auth-Token" header. Here's a complete example.

```bash
$ curl "http://localhost:5000/oauth2/access_token?client_id=...&client_secret=...&grant_type=credentials&email=user@example.com&password=..."
{ "access_token" : "JvTPWe4WsQO...uOR3x1PQ=", "expires_in" : "2013-10-20T14:16:24Z" }

$ curl -H "X-ACCESS-TOKEN:JvTPWe4WsQO...uOR3x1PQ=" "http://localhost:5000/api/v1/users"
[{"name": "Tako Man", ...}]
```

Storing credentials is not recommended, you should store the OAuth token obtained above, instead. Those expire in 60 days by default.

### Login using an XAuth Token obtained from a User's OAuth Token

If you have access to a user's social provider token (Facebook) or a social provider token and secret (Twitter), you can obtain an OAuth token in exchange for it.

```
http://localhost:5000/oauth2/access_token
    ?client_id=[your client id]
    &client_secret=[your client secret]
    &grant_type=oauth_token
    &oauth_token=[token]
    &oauth_provider=facebook

http://localhost:5000/oauth2/access_token
    ?client_id=[your client id]
    &client_secret=[your client secret]
    &grant_type=oauth_token
    &oauth_token=[token]
    &oauth_token_secret=[token secret]
    &oauth_provider=twitter
```

The response from Takoman will be identical to the "credentials" grant type above.
