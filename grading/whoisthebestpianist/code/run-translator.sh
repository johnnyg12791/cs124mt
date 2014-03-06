#!/bin/bash
# Java JDK must be 1.7 or above 
# Bash script reference:
# http://stackoverflow.com/questions/1873356/how-to-write-shell-script-to-get-jre-version
version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')

if [[ "$version" < "1.7" ]]; then
    echo Note: Java JDK 1.7 or above is needed to run the program
else
	#Compile (including Stanford POS tagger)
	mkdir classes
	javac -d classes -cp "stanford-postagger-full/stanford-postagger.jar" src/*.java

	#Run (turn on ASSERT checks)
	java -ea -cp "classes:stanford-postagger-full/stanford-postagger.jar" Translator

	#Clean up
	rm -rf classes
fi



