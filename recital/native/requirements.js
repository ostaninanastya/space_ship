db.createCollection("requirements",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "content",
      "__created__"
      ],
      properties: {	
       name: {
        bsonType: "string",
        description: "Name is required"
      },
      content: {
        bsonType: "array",
        description: "List of requirements"
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