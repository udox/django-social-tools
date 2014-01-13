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
GREEN=2e8058

convert $1 -posterize $PRE_LEVELS -threshold $THRESHOLD -gaussian-blur $BLUR_RADIUS \
    -posterize $POST_LEVELS +level-colors "#$GREEN", /tmp/stan.`basename $1`;

echo /tmp/stan.`basename $1`;
