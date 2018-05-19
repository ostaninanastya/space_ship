db.createCollection("shift_states",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "shift",
      "__created__"
      ],
      properties: {	
        timestamp: {
          bsonType: "date",
          description: "Time of shift state"
        },
        shift: {
          bsonType: "objectId",
          description: "shift is required. Ref to entity shifts"
        },
        warning_level: {
          bsonType: "string",
          description: "warning level isn't required"
        },	
        cartridges: {
          bsonType: "int",
          description: "cartridges isn't required"
        },	
        air: {
          bsonType: "int",
          description: "state of air. isn't required"
        },			
        electricity: {
          bsonType: "int",
          description: "state of electricity. isn't required"
        },	
        comment: {
          bsonType: "string",
          description: "comment isn't required"
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