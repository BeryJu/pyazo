# LDAP Authentication

pyazo supports Authentication against LDAP or Active Directory.

To configure LDAP, add the following environment variables to your deployment:

```
PYAZO_LDAP__ENABLED: true
PYAZO_LDAP__SERVER__URI='ldap://dc1.example.com'
PYAZO_LDAP__SERVER__URI: false
PYAZO_LDAP__BIND__DN: ''
PYAZO_LDAP__BIND__PASSWORD: ''
PYAZO_LDAP__SEARCH_BASE: ''
PYAZO_LDAP__FILTER: '(sAMAccountName=%(user)s)'
PYAZO_LDAP__REQUIRE_GROUP: false
```

The `require_group` setting is optional and can be used to specify the DN of a group the user has to be member of.
