# Smart Home
Custom smart home handlers

## Configuration

Place a config.ini file in the project root directory to provide config values.

```ini
[server]
port = <port>
```

## Fireplace

### Handlers

####PUT /smarthome/fireplace/start

Turn the fireplace on

**REQUEST BODY**: fireplace.__state object (optional)

####PUT /smarthome/fireplace/stop

Turn the fireplace off

**REQUEST BODY**: None

####GET /smarthome/fireplace

Get the state of the fireplace

**REPOSONSE BODY**: fireplace.__state object

####PATCH /smarthome/fireplace

Update some values of the state of the fireplace

**REQUEST BODY**: fireplace.__state (partial)
