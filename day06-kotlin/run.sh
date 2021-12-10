#!/usr/bin/bash

# To install kotlin compiler - https://kotlinlang.org/docs/command-line.html

 kotlinc ./LantenfishCalculator.kt -include-runtime -d LantenfishCalculator.jar

 java -jar LantenfishCalculator.jar example.txt
 echo ""
 java -jar LantenfishCalculator.jar data.txt