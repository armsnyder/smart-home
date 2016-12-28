#!/usr/bin/env bash

# Check that we are superuser (i.e. $(id -u) is zero)
if (( $(id -u) ))
then
    echo "This script needs to run as root"
    exit 1
fi

# define function to exit script early if it detects a failure
catch() { [[ $? -eq 0 ]] || exit 1; }

install_path="/opt/armsnyder/smarthome"
log_path="/var/armsnyder/smarthome/"
daemon_path="/Library/LaunchDaemons"
daemon_pattern="com.armsnyder.smarthome.*"
remote_repo="https://github.com/armsnyder/smart-home.git"
username=_smarthome

# create install directory
mkdir -p "${install_path}"
catch
cd "${install_path}"
catch

# clone github repository inside install directory
git clone "${remote_repo}" "${install_path}"
catch

# install python dependencies
pip install --upgrade pip
catch
pip install -r python/requirements.txt
catch

# copy launchd daemons
cp -R LaunchDaemons/* "${daemon_path}"
catch

# create a config file
cat > python/config.ini << EOF
[server]
http_port = 8032
https_port = 4432
EOF
catch

# generate ssl certificate
mkdir python/ssl
openssl req -batch -nodes -x509 -newkey rsa:2048 -keyout python/ssl/key.pem -out python/ssl/cert.pem -days 365

# create daemon user account
dscl . -create /Groups/${username}
dscl . -append /Groups/${username} PrimaryGroupID 332
dscl . -create /Users/${username}
dscl . -append /Users/${username} UniqueID 332
dscl . -append /Users/${username} PrimaryGroupID 332

# restrict files to daemon
chown -R ${username}:${username} ${install_path}

# grant permission to log files
mkdir -p "${log_path}" 2>/dev/null
chown -R ${username}:${username} ${log_path}

# load the launchd daemons to start the service
find "${daemon_path}" -name "${daemon_pattern}" -exec sudo launchctl load -w {} \;
catch

echo "Finished installing"
