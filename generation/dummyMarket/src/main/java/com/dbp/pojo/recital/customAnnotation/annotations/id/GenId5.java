package com.dbp.pojo.recital.customAnnotation.annotations.id;

import com.dbp.pojo.recital.customAnnotation.impl.id.Id5Generator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(Id5Generator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenId5 {
    //for department, locations and propertyTypes
}

