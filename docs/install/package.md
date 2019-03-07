# Installation

pyazo is a python-based application which requires Python 3.5 or newer.

The following services are also a requirement:

 - MySQL/MariaDB
 - Redis

By default, APT will install these services on the same server as pyazo is on. This can be omitted by running apt with `--no-install-recommends`.

## Add the repository

Run the following commands to add the pkg.beryju.org Apt-Repository.

```
wget -O - -q https://pkg.beryju.org/repository/raw-utils/apt/public.key | apt-key add -
echo "deb https://pkg.beryju.org/repository/apt/ beryjuorg main" >> /etc/apt/sources.list
apt update
```

After the commands finish, you can install the package for the python version shown above:

```
apt install pyazo
```

## Create a superuser

After the installation is done, you should create a superuser to access the Web-Interface. Execute the following command to create a User with Administrative rights:

```
/usr/share/pyazo/pyazo.sh createsuperuser
```
