#!/usr/bin/env bash

# define function to exit script early if it detects a failure
catch() { [[ $? -eq 0 ]] || exit 1; }

install_path="/opt/armsnyder/smarthome"
daemon_path="/Library/LaunchDaemons"
daemon_pattern="com.armsnyder.smarthome.*"

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

echo "Finished uninstalling"
