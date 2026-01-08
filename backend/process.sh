for file in `ls conv*.txt`; do
python3 command_line_query.py $file > $file.log
done
