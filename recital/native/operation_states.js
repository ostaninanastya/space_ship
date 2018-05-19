db.createCollection("operation_states",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
      "boat",
      "operation",
      "__created__"
      ],
      properties: {
        timestamp: {
          bsonType: "date",
          description: "Time of operation state"
        },
        boat: {
          bsonType: "objectId",
          description: "boat is required. Ref to entity boats"
        },
        operation: {
          bsonType: "objectId",
          description: "operation is required. Ref to entity operations"
        },
        status: {
          bsonType: "string",
          description: "status isn't required"
        },
        distance: {
          bsonType: "double",
          description: "distance isn't required"
        },
        zenith: {
          bsonType: "double"
        },
        azimuth: {
          bsonType: "double"
        },
        hydrogenium: {
          bsonType: "double"
        },
        helium: {
          bsonType: "double"
        },
        lithium: {
          bsonType: "double"
        },
        beryllium: {
          bsonType: "double"
        },
        borum: {
          bsonType: "double"
        },
        carboneum: {
          bsonType: "double"
        },
        nitrogenium: {
          bsonType: "double"
        },
        oxygenium: {
          bsonType: "double"
        },
        fluorum: {
          bsonType: "double"
        },
        neon: {
          bsonType: "double"
        },
        natrium: {
          bsonType: "double"
        },
        magnesium: {
          bsonType: "double"
        },
        aluminium: {
          bsonType: "double"
        },
        silicium: {
          bsonType: "double"
        },
        phosphorus: {
          bsonType: "double"
        },
        sulfur: {
          bsonType: "double"
        },
        chlorum: {
          bsonType: "double"
        },
        argon: {
          bsonType: "double"
        },
        kalium: {
          bsonType: "double"
        },
        calcium: {
          bsonType: "double"
        },
        scandium: {
          bsonType: "double"
        },
        titanium: {
          bsonType: "double"
        },
        vanadium: {
          bsonType: "double"
        },
        chromium: {
          bsonType: "double"
        },
        manganum: {
          bsonType: "double"
        },
        ferrum: {
          bsonType: "double"
        },
        cobaltum: {
          bsonType: "double"
        },
        niccolum: {
          bsonType: "double"
        },
        cuprum: {
          bsonType: "double"
        },
        zincum: {
          bsonType: "double"
        },
        gallium: {
          bsonType: "double"
        },
        germanium: {
          bsonType: "double"
        },
        arsenicum: {
          bsonType: "double"
        },
        selenium: {
          bsonType: "double"
        },
        bromum: {
          bsonType: "double"
        },
        crypton: {
          bsonType: "double"
        },
        rubidium: {
          bsonType: "double"
        },
        strontium: {
          bsonType: "double"
        },
        yttrium: {
          bsonType: "double"
        },
        zirconium: {
          bsonType: "double"
        },
        niobium: {
          bsonType: "double"
        },
        molybdaenum: {
          bsonType: "double"
        },
        technetium: {
          bsonType: "double"
        },
        ruthenium: {
          bsonType: "double"
        },
        rhodium: {
          bsonType: "double"
        },
        palladium: {
          bsonType: "double"
        },
        argentum: {
          bsonType: "double"
        },
        cadmium: {
          bsonType: "double"
        },
        indium: {
          bsonType: "double"
        },
        stannum: {
          bsonType: "double"
        },
        stibium: {
          bsonType: "double"
        },
        tellurium: {
          bsonType: "double"
        },
        iodium: {
          bsonType: "double"
        },
        xenon: {
          bsonType: "double"
        },
        caesium: {
          bsonType: "double"
        },
        barium: {
          bsonType: "double"
        },
        lanthanum: {
          bsonType: "double"
        },
        cerium: {
          bsonType: "double"
        },
        praseodymium: {
          bsonType: "double"
        },
        neodymium: {
          bsonType: "double"
        },
        promethium: {
          bsonType: "double"
        },
        samarium: {
          bsonType: "double"
        },
        europium: {
          bsonType: "double"
        },
        gadolinium: {
          bsonType: "double"
        },
        terbium: {
          bsonType: "double"
        },
        dysprosium: {
          bsonType: "double"
        },
        holmium: {
          bsonType: "double"
        },
        erbium: {
          bsonType: "double"
        },
        thulium: {
          bsonType: "double"
        },
        ytterbium: {
          bsonType: "double"
        },
        lutetium: {
          bsonType: "double"
        },
        hafnium: {
          bsonType: "double"
        },
        tantalum: {
          bsonType: "double"
        },
        wolframium: {
          bsonType: "double"
        },
        rhenium: {
          bsonType: "double"
        },
        osmium: {
          bsonType: "double"
        },
        iridium: {
          bsonType: "double"
        },
        platinum: {
          bsonType: "double"
        },
        aurum: {
          bsonType: "double"
        },
        hydrargyrum: {
          bsonType: "double"
        },
        thallium: {
          bsonType: "double"
        },
        plumbum: {
          bsonType: "double"
        },
        bismuthum: {
          bsonType: "double"
        },
        polonium: {
          bsonType: "double"
        },
        astatum: {
          bsonType: "double"
        },
        radon: {
          bsonType: "double"
        },
        francium: {
          bsonType: "double"
        },
        radium: {
          bsonType: "double"
        },
        actinium: {
          bsonType: "double"
        },
        thorium: {
          bsonType: "double"
        },
        protactinium: {
          bsonType: "double"
        },
        uranium: {
          bsonType: "double"
        },
        neptunium: {
          bsonType: "double"
        },
        plutonium: {
          bsonType: "double"
        },
        americium: {
          bsonType: "double"
        },
        curium: {
          bsonType: "double"
        },
        berkelium: {
          bsonType: "double"
        },
        californium: {
          bsonType: "double"
        },
        einsteinium: {
          bsonType: "double"
        },
        fermium: {
          bsonType: "double"
        },
        mendelevium: {
          bsonType: "double"
        },
        nobelium: {
          bsonType: "double"
        },
        lawrencium: {
          bsonType: "double"
        },
        rutherfordium: {
          bsonType: "double"
        },
        dubnium: {
          bsonType: "double"
        },
        seaborgium: {
          bsonType: "double"
        },
        bohrium: {
          bsonType: "double"
        },
        hassium: {
          bsonType: "double"
        },
        meitnerium: {
          bsonType: "double"
        },
        darmstadtium: {
          bsonType: "double"
        },
        roentgenium: {
          bsonType: "double"
        },
        copernicium: {
          bsonType: "double"
        },
        nihonium: {
          bsonType: "double"
        },
        flerovium: {
          bsonType: "double"
        },
        moscovium: {
          bsonType: "double"
        },
        livermorium: {
          bsonType: "double"
        },
        tennessium: {
          bsonType: "double"
        },
        oganesson: {
          bsonType: "double"
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