db.createCollection("system_tests",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "result",
      "system",
      "__created__"
      ],
      properties: {	
        timestamp: {
          bsonType: "date",
          description: "Time of system test"
        },
        system: {
          bsonType: "objectId",
          description: "Is required. Ref to entity system_types"
        },	
        result: {
          bsonType: "int",
          description: "Is required. Result of system test(number)"
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