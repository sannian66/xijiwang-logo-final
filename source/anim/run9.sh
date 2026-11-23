rm -rf i52 d52
python3 render3.py v52.html i52 "" 60 5.0 2560 &
python3 render3.py v52.html d52 "#demo" 60 14.2 2560 &
wait; ls i52 | wc -l; ls d52 | wc -l
