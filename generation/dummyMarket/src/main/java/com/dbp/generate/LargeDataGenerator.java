package com.dbp.generate;

import com.dbp.pojo.recital.*;
import io.dummymaker.export.IExporter;
import io.dummymaker.export.impl.CsvExporter;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.util.ArrayList;
import java.util.List;

public abstract class LargeDataGenerator{
    public static final int AMOUNT = 1000;
    public static void generate() {
        //systems
        List<systems> systems = new GenProduceFactory().produce(systems.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./mongo json/").withPretty().export(systems);

        //properties
        List<properties> prop = new GenProduceFactory().produce(properties.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./mongo json/").export(prop);

        //people
        List<people> pep = new GenProduceFactory().produce(people.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./mongo json/").export(pep);

        //sensors
        List<sensors> sensors = new GenProduceFactory().produce(sensors.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./mongo json/").export(sensors);

        //boats
        List<boats> boats = new GenProduceFactory().produce(boats.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./mongo json/").export(boats);


       // boatsId = generateObject(boat.class, AMOUNT);
        //new CsvExporter().withTextWrap().export(boats.class, AMOUNT);
    }


}
