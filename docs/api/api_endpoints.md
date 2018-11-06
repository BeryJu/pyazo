# Upload

## `POST /upload`

Gyazo-compatible upload endpoint. Takes 2 parameters:

#### Parameters:

 - `imagedata` Raw file data
 - `id` Currently unused field but required to be compatible with gyazo's API. Can be used to send a client identifier.

#### Returns

Returns the full URL to the uploaded file (including https://...)