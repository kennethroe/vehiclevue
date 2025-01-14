# Emporia Vehivle Vue - Home Assistant Integration

Creates a "battery" device sensor in Home Assistant to track vehicles configured in the Emporia system.  

- Requires an Emporia account with a vehicle registered in the Emporia account.
- Entity name in  HA will be set to name of vehicle as configured in Emporia.
- Integration polls Emporia every 30 minutes for each vehicle to update the battery status and charging state.  This may hit rate limits if you have multiple vehicles (not tested with multiple vehicles - Emporia has monthly rate limits).
- Extra attributes contain attributes such as charge state. 

https://my.home-assistant.io/redirect/config_flow_start?domain=vehiclevue

This integration is not affiliated with or approved by Emporia - but makes their products a bit more useful!

<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=vehiclevue" class="my badge" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg"></a>

**Example:**
<img width="1063" alt="image" src="https://github.com/user-attachments/assets/a9b8030d-703a-4262-8f63-6b20af18cf1a" />
