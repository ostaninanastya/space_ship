package com.dbp.generate;

import com.mifmif.common.regex.Generex;
import com.mifmif.common.regex.util.Iterator;
import io.dummymaker.export.impl.JsonExporter;
import io.dummymaker.factory.impl.GenProduceFactory;
import com.dbp.pojo.recital.*;

import java.util.List;

public class GenerateApplication {
    public static void main(String[] args) {
        InitDataGenerator.generate();
        LargeDataGenerator.generate();
    }
}
