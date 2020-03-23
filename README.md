# JWT Validation API

This is a lightweight API which can validate that a given JWT:

* has not expired
* has a valid signature
* is for the intended audience

You need to POST a JSON object to the API with the following structure:

```json
{
  "jwt": "<the JWT to be validated>",
  "keys": "<array of JWK>",
  "aud": "<expected audience>"
}
```

## Responses

### Valid
You'll get a 200 OK with the JSON encoded payload of the token

### Request not understood
You'll get a 400 Bad Request with an explanation of what was wrong with the request

### Invalid
You'll get a 401 Unathorized.

### All else
You'll get a 502 or 500 Server Error.