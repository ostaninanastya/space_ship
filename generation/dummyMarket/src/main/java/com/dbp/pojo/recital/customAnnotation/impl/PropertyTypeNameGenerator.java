package com.dbp.pojo.recital.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;

import java.util.ArrayList;
import java.util.List;

public class PropertyTypeNameGenerator implements IGenerator<String> {
    private static List<String> operators=new ArrayList<String>();
    private static int i = 0;

    static {
        operators.add("large tools");
        operators.add("small tools");
        operators.add("tools for cleaning");
        operators.add("furniture");
        operators.add("instruments");
    }

    @Override
    public String generate() {
        if (i == 4) i = 0;
        return operators.get(i++);
    }

    public static int getOperatorsNumber(){
        return operators.size();
    }
}