#!/bin/bash
clear

#java -mx500m -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -textFile ../plots_tryouts/26554199.txt -outputFormat xml > ../plots_tryouts/26554199.xml

cd Inputs_Outputs/plots_temp
 for i in $( ls ); do
            echo item: $i
            java -mx500m -cp /home/vionlabs/Documents/subtitle_analysis/stanford-ner-2015-04-20/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier /home/vionlabs/Documents/subtitle_analysis/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz -textFile i -outputFormat xml > ../outputs/2563340.xml
        done