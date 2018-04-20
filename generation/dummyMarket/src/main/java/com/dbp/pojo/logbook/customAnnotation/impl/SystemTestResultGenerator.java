package com.dbp.pojo.logbook.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;
import java.util.Random;

public class SystemTestResultGenerator implements IGenerator<Integer> {
    @Override
    public Integer generate() {
        int maxNumber = 100;

        Random r = new Random();
        return r.nextInt(maxNumber) + 1;
    }
}