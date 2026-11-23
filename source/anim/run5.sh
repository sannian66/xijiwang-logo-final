rm -rf i4 d4
python3 render3.py v4.html i4 "" 60 4.6 2560 &
python3 render3.py v4.html d4 "#demo" 60 13.6 2560 &
wait
ls i4 | wc -l; ls d4 | wc -l
