# LDAP Authentication

pyazo supports Authentication against LDAP or Active Directory.

To configure LDAP, uncomment the following section in the `config.yml` file:

```yml
# LDAP Authentication
ldap:
    enabled: true
    server:
        uri: 'ldap://dc1.example.com'
        tls: false
    bind:
        dn: ''
        password: ''
    search_base: ''
    filter: '(sAMAccountName=%(user)s)'
    require_group: false
```

The `require_group` setting is optional and can be used to specify the DN of a group the user has to be member of.
