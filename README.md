<h1>Emporia Vehivle Vue - Home Assistant Integration</h1>

Creates a "battery" device sensor in Home Assistant to track vehicles configured in the Emporia system.  

• Requires an Emporia account with a vehicle registered in the Emporia account.
• Entity name in  HA will be set to name of vehicle as configured in Emporia.
• Integration polls Emporia every 15 minutes for each vehicle to update the battery status and charging state.  
• Extra attributes contain attributes such as charge state. 

This integration is not affiliated with or approved by Emporia - but makes their products a bit more useful!
