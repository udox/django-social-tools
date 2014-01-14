#!/bin/bash

PRE_LEVELS=24
POST_LEVELS=2
THRESHOLD=70%
BLUR_RADIUS=4
GREEN=009e5b

OUT=/tmp/stan.`basename $1`.png
CROP=/tmp/crop.`basename $OUT`
COMPOSE=/tmp/composed.`basename $OUT`
BASE=/tmp/base.`basename $OUT`

convert $1 -posterize $PRE_LEVELS -threshold $THRESHOLD -gaussian-blur $BLUR_RADIUS \
    -posterize $POST_LEVELS +level-colors "#$GREEN", $OUT;

convert $OUT -resize '340x290^' -gravity center -crop '340x290+0+0' +repage $CROP;
convert assets/base.png -fill "#$GREEN" -pointsize 39.68 -font assets/Anthem-Bold.ttf -gravity center -draw "translate 0,240 text 0,0 '@$2'" $BASE;
convert $BASE $CROP -compose Multiply -geometry '+36+260' -composite $COMPOSE;

echo `basename $1`;
