package com.dbp.pojo.recital.customAnnotation.annotations;

import io.dummymaker.annotation.PrimeGen;
import com.dbp.pojo.recital.customAnnotation.impl.HRefGenerator;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(HRefGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenHRefToVk {
}

