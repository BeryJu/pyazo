## Reverse Proxy Configuration

To use Pyazo behind an nginx Reverse-Proxy, you can use the following configuration:

```nginx
server {
        # Server config
        listen 80;
        server_name i.domain.tld;

        # 301 to SSL
        location / {
                return 301 https://$host$request_uri;
        }
}
server {
        # Server config
        listen 443 ssl http2;
        server_name i.domain.tld;

        # SSL Certs
        ssl_certificate <ssl paths>
        ssl_certificate_key <ssl paths>

        # Disable checking of client request body size.
        client_max_body_size 0;

        # Proxy site
        location / {
                proxy_pass http://<pyazo hostname>:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-Port 443;
                proxy_set_header X-Real-IP $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-For $remote_addr;
                proxy_set_header REMOTE_ADDR $remote_addr;
                proxy_connect_timeout   10;
                proxy_read_timeout      90;
        }
}
```