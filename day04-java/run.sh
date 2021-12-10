#!/bin/bin/sh
javac -classpath bingo-solver/src -d bingo-solver/out ./bingo-solver/src/Main.java
/usr/libexec/java_home -v 11 --exec java -Dfile.encoding=UTF-8 -classpath bingo-solver/out Main ./example.txt
echo ""
/usr/libexec/java_home -v 11 --exec java -Dfile.encoding=UTF-8 -classpath bingo-solver/out Main ./data.txt
