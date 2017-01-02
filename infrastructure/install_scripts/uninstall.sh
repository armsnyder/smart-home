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
daemon_path="/Library/LaunchDaemons"
daemon_pattern="com.armsnyder.smarthome.*"
username=_smarthome

# unload daemons
find "${daemon_path}" -name "${daemon_pattern}" -exec sudo launchctl unload {} \;
catch

# delete daemon files
find "${daemon_path}" -name "${daemon_pattern}" -delete
catch

# delete install files
if [ -d "${install_path}" ]; then
    rm -R "${install_path}"
    catch
fi

# delete daemon user account
dscl . -delete /Groups/${username}
dscl . -delete /Users/${username}

echo "Finished uninstalling"
