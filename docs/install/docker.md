## Kubernetes

The recommended way to deploy pyazo on docker is on Kubernetes. To make installation easier, we provide a helm chart for this.

To install pyazo using helm on kubernetes, run the following:

```
helm repo add beryju.org https://pkg.beryju.org/repository/helm/
helm install beryju.org/pyazo
```

## Pure Docker

Pyazo can be run on pure docker. The image is `docker.pkg.beryju.org/pyazo`. The image needs to be run twice, once for the webserver and once for the background worker. The config file needs to be mounted under `/etc/pyazo/config.yml`. Uploaded files are saved under `/app/media`, which should be mounted as well.

The webserver can be started by running `manage.py web` in the Container. The process will listen on port 8000 for incoming connections.
The background-worker can be started by running `manage.py worker`.
