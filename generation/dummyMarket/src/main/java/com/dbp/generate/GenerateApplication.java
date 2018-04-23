package com.dbp.generate;

import com.dbp.generate.logbook.EnormousDataGenerator;
import com.dbp.generate.recital.InitDataGenerator;
import com.dbp.generate.recital.LargeDataGenerator;
import com.dbp.generate.relations.RelationsGenerate;
import com.dbp.pojo.relations.embedded.content;
import com.dbp.pojo.relations.requirement;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.gson.Gson;
import io.dummymaker.factory.impl.GenProduceFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class GenerateApplication {
    public static void main(String[] args) throws IOException {
        //recital
        InitDataGenerator.generate();
        //relations
        RelationsGenerate.generate();
        //logbook
        EnormousDataGenerator.generate();
    }
}
