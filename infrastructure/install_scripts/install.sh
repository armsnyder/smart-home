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

# get source path
source_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

# create install directory
mkdir -p "${install_path}"
catch
cd "${install_path}"
catch

# clone github repository inside install directory
git clone "${remote_repo}" "${install_path}"
catch

# render the config variables into the files
python infrastructure/install_scripts/render.py -rf -x .git,tests . config.ini
catch

# install python dependencies
pip install --upgrade pip
catch
pip install -r requirements.txt
catch

# copy launchd daemons
cp -R infrastructure/LaunchDaemons/* "${daemon_path}"
catch

# copy config file
cp "${source_path}/config.ini" config.ini
catch

# copy google agent creds file
cp "${source_path}/creds.data" creds.data
catch

# generate ssl certificate
ssl_path="${install_path}/frontend/ssl"
mkdir ${ssl_path}
catch
openssl req -batch -nodes -x509 -newkey rsa:2048 -keyout ${ssl_path}/key.pem -out ${ssl_path}/cert.pem -days 365
catch

# create daemon user account
dscl . -create /Groups/${username}
catch
dscl . -append /Groups/${username} PrimaryGroupID 332
catch
dscl . -create /Users/${username}
catch
dscl . -append /Users/${username} UniqueID 332
catch
dscl . -append /Users/${username} PrimaryGroupID 332
catch

# restrict files to daemon
chown -R ${username}:${username} ${install_path}
catch

# grant permission to log files
mkdir -p "${log_path}" 2>/dev/null
chown -R ${username}:${username} ${log_path}
catch

# load the launchd daemons to start the service
find "${daemon_path}" -name "${daemon_pattern}" -exec sudo launchctl load -w {} \;
catch

echo "Finished installing"
