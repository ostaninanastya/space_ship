package com.dbp.pojo.relations.customAnnotation.annotations.id;

import com.dbp.pojo.recital.customAnnotation.impl.id.BigIdGenerator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(BigIdGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenBigIdCustom {
}

