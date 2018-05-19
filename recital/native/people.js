db.createCollection("people",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "surname",
      "department",
      "specialization",
      "__created__"
      ],
      properties: {
        name: {
          bsonType: "string",
          description: "Name is required"
        },
        surname: {
          bsonType: "string",
          description: "surname is required"
        },
        patronymic: {
          bsonType: "string",
          description: "patronymic isn't required"
        },		
        department: {
          bsonType: "objectId",
          description: "department is required. Ref to entity department"
        },
        phone: {
          bsonType: "string",
          pattern : "^8 [0-9]{3} [0-9]{3}-[0-9]{2}-[0-9]{2}$",
          description: "must match with pattern. examples: +79261234567; 8(926)123-45-67; 8-926-123-45-67"

        },		
        specialization: {
          bsonType: "objectId",
          description: "specialization is required. Ref to entity specializations"
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