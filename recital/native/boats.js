db.createCollection("boats",
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
          description: "name is required"
        },
        capacity: {
          bsonType: "int",
          description: "capacity of boat"
        },
        __accessed__: {
          bsonType: "date",
          description: "time of the last access"
        },
        __created__: {
          bsonType: "date",
          description: "time of creation"
        },
        __gaps__: {
          bsonType: "array",
          description: "list of numbers",
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