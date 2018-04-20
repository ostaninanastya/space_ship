package com.dbp.pojo.logbook;

import com.dbp.pojo.logbook.customAnnotation.annotations.GenSystemTestResult;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenDouble;
import io.dummymaker.annotation.time.GenTime;
import io.dummymaker.annotation.string.GenNoun;
import io.dummymaker.annotation.string.GenPhrase;

import java.time.LocalDate;
import java.time.LocalTime;

public class shift_state {
	@GenTime(from = 2015)
    private LocalDate date;
    @GenTime(from = 2015)
    private LocalTime time;
    @GenBigIdCustom
    private Integer shift_id;
    @GenNoun
    private String warning_level;
    //because it is integer in required interval
    @GenSystemTestResult
    private Integer remaining_air;
    @GenSystemTestResult
    private Integer remaining_cartridges;
    @GenSystemTestResult
    private Integer remaining_electricity;
    @GenPhrase
    private String comment;
}
