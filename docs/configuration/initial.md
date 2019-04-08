## Initial Configuration

After you've installed Pyazo and created your superuser, there is some configuration needed to make Pyazo work.

The configuration is done in `/etc/pyazo/config.yml`. The most important setting is called `external_url`.
`external_url` dictates which URL should be used for link generation. This setting must include the protocol, e.g. `https://i.beryju.org`.

You can also optionally enable `error_report_enabled`, which sends errors directly to `sentry.services.beryju.org`.

If you prefer shorter links, you can adjust the setting `default_return_view`, which defaults to using the SHA256 of the uploaded file.
The length of links is as following:

| Function          | Length |
|-------------------|--------|
| view_sha512_short | 16     |
| view_md5          | 32     |
| view_sha256       | 64     |
| view_sha512       | 128    |