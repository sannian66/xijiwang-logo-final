#!/bin/bash
# usage: enc31.sh <framedir> <wav> <out.mp4> <N>
ffmpeg -y -v error -framerate 60 -i $1/f%04d.png -i $2 -vf scale=out_color_matrix=bt709:out_range=tv,format=yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0 -c:v libx264 -preset slow -crf 12 -c:a aac -b:a 320k -frames:v $4 $3
