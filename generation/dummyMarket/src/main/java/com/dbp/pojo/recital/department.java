package com.dbp.pojo.recital;

import com.dbp.pojo.recital.customAnnotation.annotations.GenDepartmentName;
import io.dummymaker.annotation.number.GenInteger;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.*;
import com.dbp.pojo.recital.customAnnotation.annotations.GenHRefToVk;

public class department {
    @GenEnumerate(from = 1)
    @GenInteger
    private Integer id;
    @GenDepartmentName
    private String name;
    @GenHRefToVk
    private String hrefToVkCommunity;

}
