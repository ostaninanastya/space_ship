package com.dbp.pojo.recital.customAnnotation.annotations;

import com.dbp.pojo.recital.customAnnotation.impl.StatesNameGenerator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(StatesNameGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenStatesName {
}

