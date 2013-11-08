#!/bin/bash

if [ $# -eq 0 ]
  then
    echo -e "Generates video of images called x.png.\n"
    echo -e "Usage: " $0 "ouput.mp4\n"
    exit 1
fi

ffmpeg -i %d.png -c:v libx264 -profile:v high -b:v 2000k -bufsize 2000k -preset veryslow -pix_fmt yuv420p $1
