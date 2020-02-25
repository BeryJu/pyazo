## Initial Configuration

After you've installed Pyazo and created your superuser, there is some configuration needed to make Pyazo work.

You can optionally enable `error_report_enabled`, which sends errors directly to `sentry.beryju.org`.

If you prefer shorter links, you can adjust the setting `default_return_view`, which defaults to using the SHA256 of the uploaded file.
The length of links is as following:

| Function     | Length |
|--------------|--------|
| sha512_short | 16     |
| md5          | 32     |
| sha256       | 64     |
| sha512       | 128    |
