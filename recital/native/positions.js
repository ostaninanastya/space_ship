db.createCollection("positions",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "x",
      "y",
      "z",
      "__created__"
      ],
      properties: {	
        timestamp: {
          bsonType: "date",
          description: "Time of system test"
        },
        user: {
          bsonType: "objectId",
          description: "Is required. Ref to entity people"
        },
        x: {
          bsonType: "double",
          description: "x is required"
        },
        y: {
          bsonType: "double",
          description: "y is required"
        },
        z: {
          bsonType: "double",
          description: "z is required"
        },
        speed: {
          bsonType: "double",
          description: "speed isn't required"
        },	
        attack_angle: {
          bsonType: "double",
          description: "attack_angle isn't required"
        },			
        direction_angle: {
          bsonType: "double",
          description: "direction_angle isn't required"
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