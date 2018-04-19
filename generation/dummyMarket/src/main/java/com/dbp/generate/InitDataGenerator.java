package com.dbp.generate;

import com.dbp.pojo.recital.*;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.util.List;

public abstract class InitDataGenerator {
    public static void generate(){
        //department - technical, head, security, flying, navigation(5)
        List<department> deps = new GenProduceFactory().produce(department.class, 5);
        new JsonExporter().withPretty().export(deps);

        //specialization - electrician, doctor, first engineer, second engineer, pilot, repair worker, clean worker(7)
        List<specializations> sp = new GenProduceFactory().produce(specializations.class, 7);
        new JsonExporter().withPretty().export(sp);

        //property types - large tools, small tools, tools for cleaning, furniture and instruments (5)
        List<propertyTypes> pt = new GenProduceFactory().produce(propertyTypes.class, 5);
        new JsonExporter().withPretty().export(pt);

        //states of system - ready, repair, working, out of service (4)
        List<states> states = new GenProduceFactory().produce(states.class, 4);
        new JsonExporter().withPretty().export(states);

        //system types - fuel, engine, thrusters and hydraulic(4)
        List<systemTypes> systemTypes = new GenProduceFactory().produce(systemTypes.class, 4);
        new JsonExporter().withPretty().export(systemTypes);

        //locations - top edge, bottom edge, left side, right side, back side(5)
        List<locations> locations = new GenProduceFactory().produce(locations.class, 4);
        new JsonExporter().withPretty().export(locations);
    }
}
