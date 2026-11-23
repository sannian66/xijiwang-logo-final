rm -rf i42 d42
python3 render3.py v42.html i42 "" 60 4.6 2560 &
python3 render3.py v42.html d42 "#demo" 60 13.6 2560 &
wait; ls i42 | wc -l; ls d42 | wc -l
