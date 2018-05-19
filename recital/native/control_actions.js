db.createCollection("control_actions",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "mac_address",
      "user",
      "command",
      "result",
      "__created__"
      ],
      properties: {	
        timestamp: {
          bsonType: "date",
          description: "Time of system test"
        },
        mac_address: {
          bsonType: "objectId",
          description: "Is required"
        },	
        user: {
          bsonType: "objectId",
          description: "Is required. Ref to entity people"
        },			
        command: {
          bsonType: "string",
          description: "Command is required"
        },	
        params: {
          bsonType: "string",
          description: "Params isn't required"
        },	
        result: {
          bsonType: "string",
          description: "Result is required"
        },			
        __accessed__: {
          bsonType: "date",
          description: "Time of the last access"
        },
        __created__: {
          bsonType: "date",
          description: "Time of creation is required."
        },
        __gaps__: {
          bsonType: "array",
          description: "List of numbers",
          items: {
            bsonType: "double"
          }
        },
        __cause__: {
          bsonType: [
          "string",
          "null"
          ],
          description: "The reason why the record was moved"
        }
      }
    }
  }
})