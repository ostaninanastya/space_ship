package com.dbp.generate.recital;

import com.dbp.pojo.recital.*;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.util.List;

public abstract class InitDataGenerator {
    private static final int departmentAmount = 5;
    private static final int specializationAmount = 7;
    private static final int propertyTypesAmount = 5;
    private static final int statesAmount = 4;
    private static final int systemTypesAmount = 4;
    private static final int locationsAmount = 4;

    public static void generate(){
        //init data
        List<department> deps = new GenProduceFactory().produce(department.class, departmentAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(deps);

        List<specializations> sp = new GenProduceFactory().produce(specializations.class, specializationAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(sp);

        List<propertyTypes> pt = new GenProduceFactory().produce(propertyTypes.class, propertyTypesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(pt);

        List<states> states = new GenProduceFactory().produce(states.class, statesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(states);

        List<systemTypes> systemTypes = new GenProduceFactory().produce(systemTypes.class, systemTypesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(systemTypes);

        List<locations> locations = new GenProduceFactory().produce(locations.class, locationsAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(locations);
        //large data
        LargeDataGenerator.generate();
    }
}