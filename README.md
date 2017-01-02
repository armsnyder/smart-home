# Smart Home
The house is alive!

## What To Modify

### Adding New Behavior

To add new components or new logic for exiting components, modify code in the `backend` directory.

### Expanding the IFTTT Gateway

To enable new IFTTT commands to interact with the backend, checkout the `frontend/handler.py` module's `handle_ifttt`
function.

### Expanding the Google Assistant Gateway

Expanding the capabilities of the Google Assistant integration involved changing two files. First, modify the
`frontend/action.json` document to include specs for the new commands/conversations. Then, modify the
`backend/action.py` file to handle the new commands/conversations.

## Continuous Integration

After it has been installed, the project will periodically check for updates from master and reboot the server with any 
new changes. So, updating the "production environment" is as simple as committing to master. Note: The script runs as
a daemon user with restricted permissions.

## Fireplace

### IFTTT Handlers

####PUT /smarthome/fireplace/start

Turn the fireplace on

####PUT /smarthome/fireplace/stop

Turn the fireplace off

### Google Assistant Handlers

Nothing yet
