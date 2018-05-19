db.createCollection("properties",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "type",
      "admission",
      "department",
      "__created__"
      ],
      properties: {
        name: {
          bsonType: "string",
          description: "Name is required"
        },
        type: {
          bsonType: "objectId",
          description: "Type is required. Ref to entity property_types"
        },	
        admission: {
          bsonType: "date",
          description: "Is required. Time of the admission"
        },
        comissioning: {
          bsonType: "date",
          description: "Time of the comissioning"
        },			
        department: {
          bsonType: "objectId",
          description: "department is required. Ref to entity department"
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