gcc -o energy_consumption energy_consumption.c
g++ -std=c++11 -o life_support_rating life_support_rating.cpp

./energy_consumption example.txt 5
./life_support_rating example.txt
echo ""
./energy_consumption data.txt 12
./life_support_rating data.txt
