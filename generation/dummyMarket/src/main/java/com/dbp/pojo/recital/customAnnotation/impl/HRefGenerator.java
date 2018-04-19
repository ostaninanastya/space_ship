package com.dbp.pojo.recital.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;

import java.util.ArrayList;
import java.util.List;

public class HRefGenerator implements IGenerator<String> {
    private static List<String> operators=new ArrayList<String>();
    private static int i = 0;

    static {
        operators.add("vk.com/technical_department");
        operators.add("vk.com/head_department");
        operators.add("vk.com/flying_department");
        operators.add("vk.com/security_department");
        operators.add("vk.com/navigation_department");
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