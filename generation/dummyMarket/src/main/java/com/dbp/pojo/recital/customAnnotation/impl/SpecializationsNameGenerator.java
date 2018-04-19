package com.dbp.pojo.recital.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;

import java.util.ArrayList;
import java.util.List;

public class SpecializationsNameGenerator implements IGenerator<String> {
    private static List<String> operators=new ArrayList<String>();
    private static int i = 0;

    static {
        operators.add("electrician");
        operators.add("doctor");
        operators.add("first engineer");
        operators.add("second engineer");
        operators.add("pilot");
        operators.add("repair worker");
        operators.add("clean worker");
    }

    @Override
    public String generate() {
        if (i == 6) i = 0;
        return operators.get(i++);
    }

    public static int getOperatorsNumber(){
        return operators.size();
    }
}