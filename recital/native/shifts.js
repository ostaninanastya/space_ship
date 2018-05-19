db.createCollection("shifts",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "start",
      "end",
      "department",
      "chief",
      "workers",
      "__created__"
      ],
      properties: {	
        start: {
          bsonType: "date",
          description: "Is required. Time of the shift start"
        },
        end: {
          bsonType: "date",
          description: "Is required. Time of the shift end"
        },			
        department: {
          bsonType: "objectId",
          description: "department is required. Ref to entity department"
        },
        chief: {
          bsonType: "objectId",
          description: "chief is required. Ref to entity people"
        },		
        workers: {
          bsonType: "array",
          description: "List of workers id",
          items: {
            bsonType: "objectId"
          }
        },		
        requirements: {
          bsonType: "string",
          description: "requirements for shift"
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