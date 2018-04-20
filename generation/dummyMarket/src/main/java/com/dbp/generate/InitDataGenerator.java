package com.dbp.generate;

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
        //department - technical, head, security, flying, navigation(5)
        List<department> deps = new GenProduceFactory().produce(department.class, departmentAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(deps);

        //specialization - electrician, doctor, first engineer, second engineer, pilot, repair worker, clean worker(7)
        List<specializations> sp = new GenProduceFactory().produce(specializations.class, specializationAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(sp);

        //property types - large tools, small tools, tools for cleaning, furniture and instruments (5)
        List<propertyTypes> pt = new GenProduceFactory().produce(propertyTypes.class, propertyTypesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(pt);

        //states of system - ready, repair, working, out of service (4)
        List<states> states = new GenProduceFactory().produce(states.class, statesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(states);

        //system types - fuel, engine, thrusters and hydraulic(4)
        List<systemTypes> systemTypes = new GenProduceFactory().produce(systemTypes.class, systemTypesAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(systemTypes);

        //locations - top edge, bottom edge, left side, right side, back side(5)
        List<locations> locations = new GenProduceFactory().produce(locations.class, locationsAmount);
        new JsonExporter().withPretty().withPath("./mongo json/").export(locations);
    }
}
