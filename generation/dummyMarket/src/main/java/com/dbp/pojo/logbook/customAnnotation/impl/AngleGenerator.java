package com.dbp.pojo.logbook.customAnnotation.impl;

import io.dummymaker.generator.IGenerator;
import java.util.Random;

public class AngleGenerator implements IGenerator<Double> {
    @Override
    public Double generate() {
        double maxAngle = 6.28;

        Random r = new Random();
        return r.nextDouble()*maxAngle;
    }
}