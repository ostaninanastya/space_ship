package com.dbp.pojo.logbook;

import com.dbp.pojo.logbook.customAnnotation.annotations.GenAngle;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenDouble;
import io.dummymaker.annotation.time.GenTime;
import io.dummymaker.annotation.string.GenNoun;
import io.dummymaker.annotation.string.GenCompany;
import io.dummymaker.annotation.string.GenCountry;

import java.time.LocalDate;
import java.time.LocalTime;

public class sensors_data {
	@GenTime(from = 2015)
    private LocalDate date;
    @GenTime(from = 2015)
    private LocalTime time;
    @GenBigIdCustom
    private Integer sensor_id;
    @GenCompany
    private String event;
    @GenCountry
    private String value_name;
    @GenDouble
    private String value;
    @GenNoun
    private String units;
}
