db.createCollection("departments",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "name",
      "director",
      "__created__"
      ],
      properties: {
        name: {
          bsonType: "string",
          description: "Name is required"
        },
        vk: {
          bsonType: "string",
          pattern: "^(https?://)?vk\.com/.+$",
          description: "must match with pattern. examples:https://vk.com/name_of_your_group, http://vk.com/name_of_your_group, vk.com/name_of_your_group"
        },
        director: {
          bsonType: "objectId",
          description: "Director is required. Ref to director"
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