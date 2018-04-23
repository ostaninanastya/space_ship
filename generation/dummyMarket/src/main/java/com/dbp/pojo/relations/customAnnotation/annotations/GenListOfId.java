package com.dbp.pojo.relations.customAnnotation.annotations;

import com.dbp.pojo.recital.customAnnotation.impl.id.BigIdGenerator;
import com.dbp.pojo.relations.customAnnotation.impl.ListOfIdGenerator;
import io.dummymaker.annotation.PrimeGen;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@PrimeGen(ListOfIdGenerator.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)

public @interface GenListOfId {
}

