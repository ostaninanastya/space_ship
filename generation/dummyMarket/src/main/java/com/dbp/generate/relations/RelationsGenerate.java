package com.dbp.generate.relations;

import com.dbp.pojo.recital.systems;
import com.dbp.pojo.relations.*;
import com.dbp.pojo.relations.embedded.content;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.gson.Gson;
import io.dummymaker.export.IExporter;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import static com.dbp.generate.constant.Modifier.AMOUNT;

public abstract class RelationsGenerate {
    public static void generate() throws IOException {
        //generate persons
        List<person> persons = new GenProduceFactory().produce(person.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./neo4j json/").withPretty().export(persons);
        //generate department
        List<department> departments = new GenProduceFactory().produce(department.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./neo4j json/").withPretty().export(departments);
        //generate operations
        List<operation> operations = new GenProduceFactory().produce(operation.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./neo4j json/").withPretty().export(operations);
        //generate shifts
        List<shift> shifts = new GenProduceFactory().produce(shift.class, AMOUNT);
        new JsonExporter().withPretty().withPath("./neo4j json/").withPretty().export(shifts);
        //generate requirement
        List<requirement> requirements = new GenProduceFactory().produce(requirement.class, AMOUNT);
        Gson gson = new Gson();
        File file = new File("neo4j json//requirement.json");
        FileWriter fileWriter = new FileWriter(file);
        fileWriter.write("");

        try {
            fileWriter.append("{\n" + "\t\"requirements\": [");
            for (int i = 0; i< requirements.size() - 2; i++ ) {
                fileWriter.write(gson.toJson(requirements.get(i)));
                fileWriter.write(",");
            }
            fileWriter.write(gson.toJson(requirements.get(requirements.size() - 1)) + "]\n" + "}");

            fileWriter.flush();
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
