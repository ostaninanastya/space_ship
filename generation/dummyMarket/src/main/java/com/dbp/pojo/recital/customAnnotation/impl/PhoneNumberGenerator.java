package com.dbp.pojo.recital.customAnnotation.impl;

import com.mifmif.common.regex.Generex;
import io.dummymaker.generator.IGenerator;

import java.util.Random;

public class PhoneNumberGenerator implements IGenerator<String> {

    Generex generex = new Generex("8 [0-9]{3} [0-9]{3}-[0-9]{2}-[0-9]{2}");
    //for department, locations and propertyTypes
    @Override
    public String generate() {
        String randomStr = generex.random();
        return randomStr;
    }
}