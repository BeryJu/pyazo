## Kubernetes

The recommended way to deploy pyazo on docker is on Kubernetes. To make installation easier, we provide a helm chart for this.

To install pyazo using helm on kubernetes, run the following:

```
helm repo add beryju.org https://pkg.beryju.org/repository/helm/
helm install beryju.org/pyazo --name pyazo --namespace pyazo -f <config file>
```

To configure it, you can use a config as following:

```yaml
postgresql:
  postgresqlPassword: "<password>"
  persistence:
    storageClass: standard

redis:
  password: "<password>"
  master:
    persistence:
      enabled: false

persistence:
  storageClass: standard

ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    certmanager.k8s.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/tls-acme: "true"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  tls:
    - secretName: letsencrypt-prod
      hosts:
        - <url>
  hosts:
    - <url>
  defaultHost: <url>
```

To see all possible settings you can change, refer to [https://git.beryju.org/BeryJu.org/pyazo/blob/master/helm/pyazo/values.yaml](https://git.beryju.org/BeryJu.org/pyazo/blob/master/helm/pyazo/values.yaml)

## Pure Docker

Pyazo can be run on pure docker. The image is `docker.pkg.beryju.org/pyazo`. The image needs to be run twice, once for the webserver and once for the background worker. The config file needs to be mounted under `/etc/pyazo/config.yml`. Uploaded files are saved under `/app/media`, which should be mounted as well.

The webserver can be started by running `manage.py web` in the Container. The process will listen on port 8000 for incoming connections.
The background-worker can be started by running `manage.py worker`.
