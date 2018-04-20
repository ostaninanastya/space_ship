package com.dbp.pojo.logbook;

import com.dbp.pojo.logbook.customAnnotation.annotations.GenSystemTestResult;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.time.GenTime;

import java.time.LocalDate;
import java.time.LocalTime;

public class system_test {
	@GenTime(from = 2015)
    private LocalDate date;
    @GenTime(from = 2015)
    private LocalTime time;
    @GenBigIdCustom
    private Integer system;
    @GenSystemTestResult
    private Integer result;
}
