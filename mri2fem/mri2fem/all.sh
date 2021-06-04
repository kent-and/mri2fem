#!/bin/bash

# Run all.sh script in chp3, chp4, chp5 and chp6


echo "###############################"
echo "##  Checking book softeware  ##" 
echo "###############################"
python3  chp2/test_book_software.py


echo "#######################"
echo "##  Run chp3 scripts ##" 
echo "#######################"
bash  chp3/all.sh


echo "#######################"
echo "##  Run chp4 scripts ##" 
echo "#######################"
bash  chp4/all.sh



echo "#######################"
echo "##  Run chp5 scripts ##" 
echo "#######################"
bash  chp5/all.sh


echo "#######################"
echo "##  Run chp6 scripts ##" 
echo "#######################"
bash  chp6/all.sh
