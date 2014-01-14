#!/bin/bash

# http://redmine.u-dox.com/issues/21655#note-9
#
# 1. User takes their photo
# 2. Posterize to 10 levels
# 3. Threshold 75-150
# 4. Gaussian blur 1-4 pixels
# 5. Posterize to 2 levels
# 6. New layer with correct Stan Smith green, set to Screen
#

PRE_LEVELS=10
POST_LEVELS=2
THRESHOLD=50%
BLUR_RADIUS=4
GREEN=009e5b

OUT=/tmp/stan.`basename $1`
CROP=/tmp/crop.`basename $OUT`
COMPOSE=/tmp/composed.`basename $OUT`
BASE=/tmp/base.`basename $OUT`

convert $1 -posterize $PRE_LEVELS -threshold $THRESHOLD -gaussian-blur $BLUR_RADIUS \
    -posterize $POST_LEVELS +level-colors "#$GREEN", $OUT;

# Base positioning area to frame:
#  340x290 size, 36 from left 252 from top
#
# We generate a "filtered" image, then create a blank base with the twitter handle
# and then we compose the lot. We store all 3 so the artworkers can use what they
# think they can work with the most
convert $OUT -resize '340x290^' -gravity center -crop '340x290+0+0' +repage $CROP;
convert assets/base.png -fill "#$GREEN" -pointsize 39.68 -font assets/Anthem-Bold.ttf -gravity center -draw "translate 0,240 text 0,0 '@$2'" $BASE;
convert $BASE $CROP -compose Multiply -geometry '+36+250' -composite $COMPOSE;

# Echo out the saved file, we'll use this back in the python code to generate
# the filenames as above for assigning to a tweet object
echo `basename $1`;
