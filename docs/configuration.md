# Configuration

pyazo is configured through environment variables, which can be saved in a `.env` file in the same directory as your `docker-compose.yml` file.
After changing any of these options, run `docker-compose up -d` to apply them.

## Secret Key

This key is used to create cookies. Use a website like [this](https://miniwebtool.com/django-secret-key-generator/) to generate a key.

```
PYAZO_SECRET_KEY=some-key-that-should-be-really-long
```

## Error Reporting

It is recommended to enable Error-reporting, as it drastically improves bug reporting and fixing:

```
PYAZO_ERROR_REPORTING=true
```

## Link Settings

If you prefer shorter links, you can adjust the setting `PYAZO_DEFAULT_RETURN_VIEW`, which defaults to using the SHA256 of the uploaded file.
The length of links is as following:

| Setting                                  | Length |
|------------------------------------------|--------|
| `PYAZO_DEFAULT_RETURN_VIEW=sha512_short` | 16     |
| `PYAZO_DEFAULT_RETURN_VIEW=md5`          | 32     |
| `PYAZO_DEFAULT_RETURN_VIEW=sha256`       | 64     |
| `PYAZO_DEFAULT_RETURN_VIEW=sha512`       | 128    |

## Auto Claim

Auto Claim automatically claims uploads to the first visitor that is logged in. Enable by add thing:

```
PYAZO_AUTO_CLAIM_ENABLED=true
```

## LDAP Authentication

pyazo supports Authentication against LDAP or Active Directory.

To configure LDAP, add the following environment variables to your `.env` file:

```
PYAZO_LDAP__ENABLED=true
PYAZO_LDAP__SERVER__URI=ldap://dc1.example.com
PYAZO_LDAP__SERVER__TLS=false
PYAZO_LDAP__BIND__DN=bind-user
PYAZO_LDAP__BIND__PASSWORD=bind-password
PYAZO_LDAP__SEARCH_BASE=
PYAZO_LDAP__FILTER=(sAMAccountName=%(user)s)
PYAZO_LDAP__REQUIRE_GROUP=false
```

The `%(user)s` placeholder in `PYAZO_LDAP__FILTER` is replaced by the username entered in the login form.

The `PYAZO_LDAP__REQUIRE_GROUP` setting is optional and can be used to specify the DN of a group the user has to be member of.

## OIDC Authentication

pyazo supports Authentication against any OpenID-Connect compatible provider.

To configure OIDC, add the following environment variables to your `.env` file:

```
PYAZO_OIDC__CLIENT_ID=foo
PYAZO_OIDC__CLIENT_SECRET=bar
PYAZO_OIDC__AUTHORIZATION_URL=https://<your provider>/application/oidc/authorize
PYAZO_OIDC__TOKEN_URL=https://<your provider>/application/oidc/token
PYAZO_OIDC__USER_URL=https://<your provider>/application/oidc/userinfo
```

The Callback URL of pyazo is `<pyazo URL>/oidc/callback/`.
