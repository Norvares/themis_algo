for ((  i = 1 ;  i <= 10;  i++  ))
do
    python DBConnector.py -l 1000 -tk (i*10) -m 100000 -pp NounsLemma
done
