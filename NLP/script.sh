filename=$1_"nlp.py"
echo "running nlp module "$filename
python $filename
echo "calculating tdidf"
python tfidf_log.py $1
echo "generating csv file"
python tfidf_csv.py $1
rm tdid-log-$1.csv