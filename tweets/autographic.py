import subprocess
import requests
import os
from django.core.files import File


def generator(tweet):
    """
        Generate an automatic version using imagemagick that may be suitable
        to ease artworker load. Also create a blank base with the handle and
        a fully composed one which may be tweeted back.
    """
    url = tweet.image_url
    tmp_file = os.path.join('/tmp', os.path.basename(url))
    with open(tmp_file, 'wb') as img:
        img.write(requests.get(url).content)

    # Generate various adjustments - this is a little clunky but works ok (ideally)
    # we would make the attributes a FK now on the model rather than _1, _2 etc
    for cnt in range(1, 4):

        stan_process = subprocess.Popen(['tweets/scripts/stanify_%d.sh' % cnt, tmp_file, tweet.handle], stdout=subprocess.PIPE)
        out, err = stan_process.communicate()

        output = out.strip()

        auto_file = os.path.join('/tmp/', 'stan.%s.png' % output)
        composed_file = os.path.join('/tmp/', 'composed.stan.%s.png' % output)

        getattr(tweet, 'auto_photoshop_%d' % cnt).save(os.path.basename(auto_file), File(open(auto_file)))
        getattr(tweet, 'auto_compose_%d' % cnt).save(os.path.basename(composed_file), File(open(composed_file)))

        if cnt == 1:
            base_file = os.path.join('/tmp/', 'base.stan.%s.png' % output)
            tweet.auto_base.save(os.path.basename(base_file), File(open(base_file)))

