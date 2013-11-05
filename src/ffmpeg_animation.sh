#!/bin/bash

if [ $# -eq 0 ]
  then
    echo -e "Generates video of images called x.png.\n"
    echo -e "Usage: " $0 "ouput.mp4\n"
    exit 1
fi

ffmpeg -i %d.png -c:v libx264 -pix_fmt yuv420p $1
