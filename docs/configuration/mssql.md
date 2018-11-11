# Microsoft SQL Server

MSSQL is not officailly supported, but can still be used. To install support for MSSQL, run the following commands:

```
cd /usr/share/pyazo
source env/bin/activate
pip install django-mssql
deactivate
```

Afterwards, adjust `/etc/pyazo/config.d/database.yml` and replace `django.db.backends.mysql` with `sqlserver_ado`. Also change the `host` property to `<database server>\\<database>`. More information can be found under https://django-mssql.readthedocs.io/en/latest/index.html