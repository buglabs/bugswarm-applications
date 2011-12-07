var participationKey = "0f115574eb6bddd8a4c43f4454ea9f9507b6bdb9";
var resourceID = "d00884c1eb2d2ee6d886da0407028e52fd0ee188";
var swarmID = "caa6343db41ce9359c76a4d0b066e34d27e47eb0";

SWARM.connect({apikey: participationKey,
               resource: resourceID,
               swarms: [swarmID],

               // callbacks
               onconnect:
                   function onConnect() {
                       console.log("Connected to swarm: " + swarmID);                       
                   },
               onpresence:
                   function onPresence(presence) {
                       presenceObj = JSON.parse(presence);
                       if (isSwarmPresence(presenceObj)) {
                           console.log("Presence: " + presence);
                           if (!isSelfPresence(presenceObj)) {
                               sendCapabilities(presenceObj.presence.from.resource);
                           }
                       }
                   },
               onmessage:
                   function onMessage(message) {
                       messageObj = JSON.parse(message);
                       if (isPrivateMessage(messageObj)) {
                           console.log("Message: " + message);
                       }
                   }
              });

isSwarmPresence = function(presenceObj) {
    if (presenceObj.presence.from.swarm) {
        return true;
    } else {
        return false;
    }    
};

isSelfPresence = function(presenceObj) {
    if (presenceObj.presence.from.resource == resourceID) {
        return true;
    } else {
        return false;
    }
};

sendCapabilities = function(resource) {
    var payload = {"capabilities": {"feeds": ["Location", "Acceleration"], "modules": {"slot1": "LCD", "slot2": "GPS"}}};
    console.log("Sending capabilities to resource: " + resource);
    SWARM.send(payload, [{"swarm": swarmID, "resource": resource}]);
};

isPrivateMessage = function(messageObj) {
    if (messageObj.message.public == false) {
        return true;
    } else {
        return false;
    }
};