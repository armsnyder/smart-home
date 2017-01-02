#!/usr/bin/env bash

# get source path
source_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

# start google agent
cd "${source_path}" && gactions preview --invocation_name "${google.invocation_name}" --action_package \
"${source_path}/frontend/action.json" --preview_mins 2147483647

# start the server
python "${source_path}/frontend/server.py"
