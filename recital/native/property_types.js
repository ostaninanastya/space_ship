db.createCollection("property_types",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "__created__"
      ],
      properties: {
        name: {
          bsonType: "string",
          description: "Name is required"
        },
        description: {
          bsonType: "string",
          description: "Description of property type"
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