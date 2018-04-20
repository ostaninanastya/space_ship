package com.dbp.generate.relations;

import com.dbp.pojo.recital.*;
import com.dbp.pojo.relations.requirement;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.util.List;

public abstract class RelationsGenerate {
    public static final int AMOUNT = 1000;
    public static void generate() {
        //systems
        List<requirement> requirement = new GenProduceFactory().produce(requirement.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./graph json/").withPretty().export(requirement);
    }
}
