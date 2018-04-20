package com.dbp.pojo.logbook;

import com.dbp.pojo.logbook.customAnnotation.annotations.GenSystemTestResult;
import com.dbp.pojo.recital.customAnnotation.annotations.id.GenBigIdCustom;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.time.GenTime;
import io.dummymaker.annotation.string.GenCity;
import io.dummymaker.annotation.string.GenPhrase;
import io.dummymaker.annotation.string.GenNick;

import java.time.LocalDate;
import java.time.LocalTime;

public class control_action {
	@GenTime(from = 2015)
    private LocalDate date;
    @GenTime(from = 2015)
    private LocalTime time;
    @GenBigIdCustom
    private Integer user_id;
    @GenInteger
    private Integer mac_address;
    @GenCity
    private String command;
    @GenPhrase
    private String params;
    @GenNick
    private String result;
}
