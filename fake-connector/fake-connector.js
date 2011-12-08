var participationKey, resourceID, swarmID;
participationKey = "0f115574eb6bddd8a4c43f4454ea9f9507b6bdb9";
resourceID = "d00884c1eb2d2ee6d886da0407028e52fd0ee188";
swarmID = "caa6343db41ce9359c76a4d0b066e34d27e47eb0";

// send functions
var announceConnector = function() {
    var payload;    
    payload = {"status_announcement": "connector"};
    console.log("Announcint connector status");
    SWARM.send(payload);
};

var sendCapabilities = function(from) {
    var payload;
    payload = {"capabilities": {"feeds": ["Location", "Acceleration"], "modules": {"slot1": "LCD", "slot2": "GPS"}}};
    console.log("Sending private capabilities to resource: " + from.resource);
    SWARM.send(payload, [{swarm: "caa6343db41ce9359c76a4d0b066e34d27e47eb0", resource: from.resource}]);
};

var sendFeedResponse = function(from, payload) {
    console.log("TODO: Send feed response to: " + from.resource);
};

//conditionals
var isConnectorInterest = function(payload) {
    if (payload.status_announcement && (payload.status_announcement === "connector-interest")) {
        return true;
    } else {
        return false;
    }
};

var isSwarmPresence = function(from) {
    if (from.swarm) {
        return true;
    } else {
        return false;
    }    
};

var isPublicMessage = function(publicVal) {
    if (publicVal === true) {
        return true;
    } else {
        return false;
    }
};

var isPrivateMessage = function(publicVal) {
    if (publicVal === false) {
        return true;
    } else {
        return false;
    }
};

var isFeedRequest = function(payload) {
    if (payload.type && payload.feed) {
        return true;        
    } else {
        return false;
    }
};

//main
SWARM.connect({apikey: participationKey,
               resource: resourceID,
               swarms: [swarmID],

               // callbacks
               onconnect:
                   function onConnect() {
                       console.log("Connected to swarm: " + swarmID);
                       announceConnector();
                   },
               onpresence:
                   function onPresence(presence) {
                       var presenceObj, from, type;
                       
                       presenceObj = JSON.parse(presence);                     
                       from = presenceObj.presence.from;
                       type = presenceObj.presence.type;
        
                       if (isSwarmPresence(from)) {
                           console.log("Presence: " + presence);
                       }
                   },
               onmessage:
                   function onMessage(message) {
                       var messageObj, from, payload, publicVal;
               
                       messageObj = JSON.parse(message);
                       from = messageObj.message.from;
                       payload = messageObj.message.payload;
                       publicVal = messageObj.message.public;

                       if (isPublicMessage(publicVal)) {
                           if (isConnectorInterest(payload)) {
                               sendCapabilities(from);
                           }
                       }

                       if (isPrivateMessage(publicVal)) {
                           console.log("Private Message: " + message);
                           if (isFeedRequest(payload)) {
                               sendFeedResponse(from, payload);
                           }
                       }
                   }
              });