#!/usr/bin/env bash

# define function to exit script early if it detects a failure
catch() { [[ $? -eq 0 ]] || exit 1; }

install_path="/opt/armsnyder/smarthome"

cd ${install_path}

# update remote master reference
git fetch origin master
catch
local_sha=$(git rev-parse master)
remote_sha=$(git rev-parse origin/master)

# check if remote and local differ
if [ ! ${local_sha} = ${remote_sha} ]; then
    # update all files to match remote master
    git reset --hard origin/master
    catch
    # render the config variables into the files
    python infrastructure/install_scripts/render.py -rf -x .git,tests . config.ini
    catch
    # get the process ID of the running server
    pid=$(sudo launchctl list | grep "com.armsnyder.smarthome.server" | awk '{print $1}')
    catch
    # kill the server if it is running
    [[ "${pid}" = "-" ]] || kill ${pid}
    catch
    echo "Loaded latest version ${remote_sha}"

fi
