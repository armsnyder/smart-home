#!/usr/bin/env bash

# define function to exit script early if it detects a failure
catch() { [[ $? -eq 0 ]] || exit 1; }

install_path="/opt/armsnyder/smarthome"
daemon_path="/Library/LaunchDaemons"
daemon_pattern="com.armsnyder.smarthome.*"
remote_repo="https://github.com/armsnyder/smart-home.git"

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
port = 8032
EOF
catch

# load the launchd daemons to start the service
find "${daemon_path}" -name "${daemon_pattern}" -exec sudo launchctl load -w {} \;
catch

echo "Finished installing"
