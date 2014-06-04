API
===

- [Infrastructure](#infrastructure)
- [Implementation](#implementation)
- [Playing with the API](#playing-with-the-api)
- [Errors](#errors)

Infrastructure
--------------

The Santa API uses [Eve](http://python-eve.org/)  as an infrastructure for
most of the endpoints, and implements underlying [Flask](http://flask.pocoo.org/)
routes for some customized endpoints/features.

Implementation
--------------

Eve API code lives in `santa/apps/api`, and other endpoints live in
`santa/apps/*` as [Flask blueprints](http://flask.pocoo.org/docs/blueprints/).

Playing with the API
--------------------

Get an API key. The values below use the Rudy Web Application keys.

```bash
curl "http://localhost:5000/api/v1/xapp_token?client_id=55050a745ff16a8114b8&client_secret=752dc05799b6fec555f5436a512fccdb"
```

This will give you an `xapp_token` in the output, and you can use the token
to access endpoints that does not require log in. You can specify the token
either in the query string or in the X-XAPP-TOKEN header.

```
curl http://localhost:5000/api/v1/users?xapp_token=[xapp token]
curl http://localhost:5000/api/v1/users -H "X-XAPP-TOKEN:[xapp token]"
```

For endpoints that requires log in, you will need an access token. Please see
the [API Authentication](api_authentication.md) for more details. Use the
access token similar to xapp token to access user-related endpoints

```
curl http://localhost:5000/api/v1/me?access_token=[access token]
curl http://localhost:5000/api/v1/me -H "X-ACCESS-TOKEN:[access token]"
```

Tests
-----
TODO

Authentication Strategy
-----------------------
TODO

API Caching Strategy
--------------------
TODO

JSON Caching Strategy
---------------------
TODO

Logging Strategy
----------------
TODO

Model Identity
--------------
TODO

JSON Formats
------------
TODO

Model Permissions
-----------------
TODO

JSONP
-----
TODO

Retrieving Large Collections
----------------------------
TODO

Sampling from Collections
-------------------------
TODO

Sorting Collections
-------------------
TODO

Plucking IDs
------------
TODO

Errors
------

Santa attempts to use appropriate HTTP status codes to indicate the general class of problem.

* *400 (Bad Request)* : Any case where a parameter is invalid, a required parameter is missing or any other parameter-related error explicitly handled. For example, a POST to */api/v1/me/password* with the same password as the current one will cause a 400.
* *401 (Unauthorized)* : The requester does not hold a valid authentication token or invalid credentials were specified. For example, a POST to */api/v1/xapp_token* with an invalid *client_secret* will cause a 401.
* *403 (Forbidden)* : The requesting user does not have access to the requested resource. For example, a POST to */api/v1/me/password* with an invalid current password will cause a 403.
* *404 (Not Found)* : The requested resource does not exist. For example, a GET for */api/v1/users/invalid* will result in a 404 since there is no user with the identity of *invalid*.
* *500 (Internal Server Error)* : The service encountered an unexpected error. This is likely a bug and should be reported to it@takoman.co.

All API errors contain a JSON with the following fields.

* *status* : `error`.
* *message* : can be a humanly readable error message string, or a dict from Eve validation errors.
* *backtrace* : source of the error for debugging (in development environments only).

Some API error examples:

Eve auth error
```python
{
  "message": "please provide proper credentials",
  "status": "error"
}
```

Eve validation error
```python
{
  "status": "error",
  "message":
    {
      "password": "min length is 8",
      "email": "value does not match regex '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'"
    }
}
```

Bad request API error
```python
{
  "message": "missing password",
  "status": "error"
}
```
