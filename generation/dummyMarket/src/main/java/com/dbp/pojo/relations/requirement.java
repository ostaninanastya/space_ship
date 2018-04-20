package com.dbp.pojo.relations;

import com.dbp.pojo.relations.embedded.content;
import io.dummymaker.annotation.collection.GenList;
import io.dummymaker.annotation.collection.GenMap;
import io.dummymaker.annotation.special.GenEmbedded;
import io.dummymaker.annotation.special.GenEnumerate;
import io.dummymaker.annotation.string.GenName;

import java.util.List;

public class requirement {
    @GenEnumerate(from = 1)
    private Integer ident;
    @GenName
    private String name;
    @GenEmbedded()
    private content content;
   // @GenList
    //private List operations;
    //@GenList
    //private List shifts;
}
