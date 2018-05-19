db.createCollection("operations",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "start",
      "end",
      "head",
      "executors",
      "__created__"
      ],
      properties: {	
       name: {
        bsonType: "string",
        description: "Name is required"
      },
      start: {
        bsonType: "date",
        description: "Is required. Time of the operation start"
      },
      end: {
        bsonType: "date",
        description: "Is required. Time of the operation end"
      },	
      head: {
        bsonType: "objectId",
        description: "chief is required. Ref to entity people"
      },			
      executors: {
        bsonType: "array",
        description: "List of executors id",
        items: {
          bsonType: "objectId"
        }
      },		
      requirements: {
        bsonType: "objectId",
        description: "is required. Ref to entity requirements"
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