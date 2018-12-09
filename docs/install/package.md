Pyazo is a python-based application. There are 2 different packages, one for Python 3.5.x and one for Python 3.6.x. To find out what version you have, run this:

```
python3 -c 'import sys;print(sys.version)'
```

## Add the repository

Run the following commands to add the pkg.beryju.org Apt-Repository.

```
wget -O - -q https://pkg.beryju.org/repository/raw-utils/apt/public.key | apt-key add -
echo "deb https://pkg.beryju.org/repository/apt/ beryjuorg main" >> /etc/apt/sources.list
apt update
```

After the commands finish, you can install the package for the python version shown above:

```
apt install pyazo-python3.5 # or pyazo-python3.6
```

## Create a superuser

After the installation is done, you should create a superuser to access the Web-Interface. Execute the following command to create a User with Administrative rights:

```
/usr/share/pyazo/pyazo.sh createsuperuser
```
