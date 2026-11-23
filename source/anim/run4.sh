rm -rf v3l v3d
python3 render3.py v3.html v3l "" 60 7.5 2560 &
python3 render3.py v3.html v3d "#dark" 60 7.5 2560 &
wait
ls v3l | wc -l; ls v3d | wc -l
