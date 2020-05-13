file=$1
bn="${file##*/}"

python makeDiffBindSheet.py diffBindTemplate.txt $file > diffBind_${bn//.bed/.txt}