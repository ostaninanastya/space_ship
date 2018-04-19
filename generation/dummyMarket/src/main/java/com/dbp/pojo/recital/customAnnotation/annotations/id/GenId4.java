package com.dbp.pojo.recital.customAnnotation.annotations.id;

import com.dbp.pojo.recital.customAnnotation.impl.id.Id4Generator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(Id4Generator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenId4 {
    //for states, system types
}

