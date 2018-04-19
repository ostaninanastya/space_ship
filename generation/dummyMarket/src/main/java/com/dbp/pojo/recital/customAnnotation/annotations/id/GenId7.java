package com.dbp.pojo.recital.customAnnotation.annotations.id;

import com.dbp.pojo.recital.customAnnotation.impl.id.Id4Generator;
import com.dbp.pojo.recital.customAnnotation.impl.id.Id7Generator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(Id7Generator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenId7 {
    //for states, system types
}

