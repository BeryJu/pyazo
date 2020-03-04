# pyazo
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FBeryJu%2Fpyazo.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FBeryJu%2Fpyazo?ref=badge_shield)


![](https://github.com/BeryJu/pyazo/workflows/pyazo-ci/badge.svg)

Documentation: https://beryju.github.io/pyazo/

## Quick instance

```
# Optionally enable Error-reporting
# export PYAZO_ERROR_REPORTING=true
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FBeryJu%2Fpyazo.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FBeryJu%2Fpyazo?ref=badge_large)