db.createCollection("systems",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "type",
      "launched",
      "checked",
      "supervisor",
      "state",
      "__created__"
      ],
      properties: {
        name: {
          bsonType: "string",
          description: "Name is required"
        },
        type: {
          bsonType: "objectId",
          description: "Type is required. Ref to entity system_types"
        },
        serial_number: {
          bsonType: "double",
          description: "Serial number of system"
        },		
        launched: {
          bsonType: "date",
          description: "Is required. Time of the launch"
        },
        checked: {
          bsonType: "date",
          description: "Is required. Time of the last check"
        },	
        supervisor: {
          bsonType: "objectId",
          description: "supervisor is required. Ref to entity people"
        },		
        state: {
          bsonType: "objectId",
          description: "state is required. Ref to entity system_states"
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