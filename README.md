# Smart Home
Custom smart home handlers

## Fireplace

### Handlers

####POST /smarthome/fireplace/start

Turn the fireplace on

**REQUEST BODY**: FireplaceState object (optional)

####POST /smarthome/fireplace/stop

Turn the fireplace off

**REQUEST BODY**: None

####GET /smarthome/fireplace

Get the state of the fireplace

**REPOSONSE BODY**: FireplaceState object

####PUT /smarthome/fireplace

Update some values of the state of the fireplace

**REQUEST BODY**: FireplaceState object (partial)