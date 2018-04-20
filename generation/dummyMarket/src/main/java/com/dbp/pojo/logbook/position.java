package com.dbp.pojo.logbook;

import com.dbp.pojo.logbook.customAnnotation.annotations.GenAngle;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenDouble;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;
import java.time.LocalTime;

public class position {
	@GenTime(from = 2015)
    private LocalDate date;
    @GenTime(from = 2015)
    private LocalTime time;
    @GenDouble
    private Double x;
    @GenDouble
    private Double y;
    @GenDouble
    private Double z;
    @GenDouble
    private Double speed;
    @GenAngle
    private Double attack_angle;
    @GenAngle
    private Double direction_angle;
}
