#! /usr/bin/env bash

echo "Algorytm sklearn.RandomForestClassifier."
echo "Zbiór przykładów wina."
echo "Pięć iteracji dla każdej liczby dzrew."
for i in 5 10 15
do
    echo "Liczba drzew: " $i
    ./PythonTestForest.py winequality-red-values.csv $i
done;

echo "Implementacja UMA:"
echo "Zbiór przykładów wina, turniej 20 testów."
echo "./UMArandomForest.py winequality-red-values.csv numeric 20"
./UMArandomForest.py winequality-red-values.csv numeric 20


echo "Implementacja UMA:"
echo "Zbiór przykładów grzybów, turniej 20 testów."
echo "./UMArandomForest.py agaricus-lepiota-combined2.dat discrete 20"
./UMArandomForest.py agaricus-lepiota-combined2.dat discrete 20


echo "Implementacja UMA:"
echo "Zbiór przykładów mieszkań w Bostonie."

# UWAGA: długi czas pracy dla 0:
# 0 = turniej wszystkich możliwych
for i in 2 10 20 0
do
    echo "Liczność turnieju: " $i
    ./UMArandomForest.py BostonHousing.txt discrete $i
done;
