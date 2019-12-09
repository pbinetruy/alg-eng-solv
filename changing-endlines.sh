#!/bin/bash
 pathtorandom=$1
 pathtodimacs=$2
 pathtosnap=$3
 
 echo changing-endlines.sh running...
 echo if error check if there is a / at the end of your path
 
 sed -i 's/\r//' benchmark.sh
 echo changing line endings in benchmark.sh
 
 sed -i 's/\r//' benchmark_small.sh
 echo changing line endings in benchmark_small.sh
 
 sed -i 's/\r//' benchmark_super_small.sh
 echo changing line endings in benchmark_super_small.sh
 
 
 
 
 
echo changing line endings in $pathtorandom

 INPUTFILES=$pathtorandom*.input
 SOLFILES=$pathtorandom*.solution
 
for f in $INPUTFILES
do
  sed -i 's/\r//' $f
done
for f in $SOLFILES
do
  sed -i 's/\r//' $f
done

echo changed line endings in $pathtorandom
 
 
 
 
 
echo changing line endings in $pathtodimacs

 INPUTFILES=$pathtodimacs*.dimacs
 SOLFILES=$pathtodimacs*.solution
 
for f in $INPUTFILES
do
  sed -i 's/\r//' $f
done
for f in $SOLFILES
do
  sed -i 's/\r//' $f
done

echo changed line endings in $pathtodimacs
 
 
 
 
 
echo changing line endings in $pathtosnap

 INPUTFILES=$pathtosnap*.dimacs
 SOLFILES=$pathtosnap*.solution
 
for f in $INPUTFILES
do
  sed -i 's/\r//' $f
done
for f in $SOLFILES
do
  sed -i 's/\r//' $f
done

echo changed line endings in $pathtosnap