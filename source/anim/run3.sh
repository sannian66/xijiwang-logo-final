rm -rf hl hd
python3 render3.py v2.html hl "" &
python3 render3.py v2.html hd "#dark" &
wait
ls hl | wc -l; ls hd | wc -l
