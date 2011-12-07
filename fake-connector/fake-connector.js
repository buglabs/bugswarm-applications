var participationKey = "0f115574eb6bddd8a4c43f4454ea9f9507b6bdb9";
var resourceID = "d00884c1eb2d2ee6d886da0407028e52fd0ee188";
var swarmID = "caa6343db41ce9359c76a4d0b066e34d27e47eb0";

//main
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
                       var presenceObj = JSON.parse(presence);
                     
                       var from = presenceObj.presence.from;
                       var type = presenceObj.presence.type;
        
                       if (isSwarmPresence(from)) {
                           console.log("Presence: " + presence);
                           if (!isSelfPresence(from) && !isPresenceUnavailable(type)) {
                               sendCapabilities(from);
                           }
                       }
                   },
               onmessage:
                   function onMessage(message) {
                       var messageObj = JSON.parse(message);

                       var from = messageObj.message.from;
                       var payload = messageObj.message.payload;
                       var publicVal = messageObj.message.public;

                       if (isPrivateMessage(publicVal)) {
                           console.log("Message: " + message);
                           if (isFeedRequest(payload)) {
                               sendFeedResponse(from, payload);
                           }
                       }
                   }
              });

sendCapabilities = function(from) {
    var payload = {"capabilities": {"feeds": ["Location", "Acceleration"], "modules": {"slot1": "LCD", "slot2": "GPS"}}};
    console.log("Sending capabilities to resource: " + from.resource);
    SWARM.send(payload, [{"swarm": swarmID, "resource": from.resource}]);
};

sendFeedResponse = function(from, payload) {
    console.log("Will send feed response to: " + from.resource);
    console.log("Will send feed response with feed: " + payload.feed);
};

//conditionals
isSwarmPresence = function(from) {
    if (from.swarm) {
        return true;
    } else {
        return false;
    }    
};

isSelfPresence = function(from) {
    if (from.resource == resourceID) {
        return true;
    } else {
        return false;
    }
};

isPresenceUnavailable = function(type) {    
    if (type && (type == "unavailable")) {
        return true;
    } else {
        return false;
    }
};

isPrivateMessage = function(publicVal) {
    if (publicVal == false) {
        return true;
    } else {
        return false;
    }
};

isFeedRequest = function(payload) {
    if (payload.type && payload.feed) {
        return true;        
    } else {
        return false;
    }
};