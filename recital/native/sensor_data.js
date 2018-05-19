db.createCollection("sensor_data",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "source",
      "event",
      "value",
      "__created__"
      ],
      properties: {	
        timestamp: {
          bsonType: "date",
          description: "Time of sensor data"
        },
        source: {
          bsonType: "objectId",
          description: "source is required"
        },
        event: {
          bsonType: "string",
          description: "event is required"
        },	
        meaning: {
          bsonType: "string",
          description: "meaning isn't required"
        },	
        value: {
          bsonType: "double",
          description: "value is required"
        },		
        units: {
          bsonType: "string",
          description: "units isn't required"
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