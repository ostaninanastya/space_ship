package com.dbp.pojo.logbook.customAnnotation.annotations;

import com.dbp.pojo.logbook.customAnnotation.impl.SystemTestResultGenerator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(SystemTestResultGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenSystemTestResult {
}

