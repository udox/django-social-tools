import twitter
import instagram

from dateutil.parser import parse as date_parse


class SocialPost(object):
    """
        Base class to represent a social post. Any derived classes should
        return all the attributes below
    """

    content = None
    created_at = None
    post_url = None
    image_url = None
    handle = None
    followers = None
    user_joined = None
    profile_image = None
    post_source = None  # This could be inferred but we'll be explicit for now

    def __init__(self, obj):
        self._obj = obj

    @property
    def uid(self):
        """
            The uid is commonly set to _id_ on the object in most API implementations
        """
        return self._obj.id


class TwitterPost(SocialPost):

    def get_image_url(self):
        """
            Try and extract an image url from a tweet - our preference is for
            the offical twitter attached entity, failing that look for twitpic
        """

        source = None

        try:
            source, image_url = 'twitter', self._obj.media[0]['media_url']

        except IndexError:
            try:
                expanded_url = self._obj.urls[0].expanded_url

                if 'twitpic' in expanded_url or 'pbs.twimg.com' in expanded_url:
                    source, image_url = 'twitpic', self._obj.urls[0].expanded_url
                else:
                    image_url = None

            except IndexError:
                image_url = None

        return image_url

    @property
    def content(self):
        return self._obj.text

    @property
    def post_source(self):
        return 'twitter'

    @property
    def created_at(self):
        return date_parse(self._obj.created_at)

    @property
    def post_url(self):
        return 'http://twitter.com/{0}/status/{1}'.format(self.handle, self.uid)

    @property
    def image_url(self):
        return self.get_image_url()

    @property
    def handle(self):
        return self._obj.user.screen_name

    @property
    def followers(self):
        return self._obj.user.followers_count

    @property
    def user_joined(self):
        return date_parse(self._obj.user.created_at)

    @property
    def profile_image(self):
        return self._obj.user.profile_image_url


class InstagramPost(SocialPost):

    @property
    def content(self):
        try:
            return self._obj.caption.text
        except AttributeError:
            return None

    @property
    def post_source(self):
        return 'instagram'

    @property
    def created_at(self):
        return self._obj.created_time

    @property
    def post_url(self):
        return self._obj.link

    @property
    def image_url(self):
        return self._obj.images['standard_resolution'].url

    @property
    def handle(self):
        return self._obj.user.username

    @property
    def followers(self):
        # Unknown via instagram api (at least as of writing 28/01/14)
        return None

    @property
    def user_joined(self):
        # Also unknown
        return None

    @property
    def profile_image(self):
        return self._obj.user.profile_picture


class SocialSearchFacade(object):
    """
        A facade around the various social media APIs we will use so that
        the sync tool and other jobs have a common interface
    """

    def __init__(self, account):
        self.account = account

    def get_api(self):

        if self.account.type == 'twitter':

            return twitter.Api(
                consumer_key=self.account.consumer_key,
                consumer_secret=self.account.consumer_secret,
                access_token_key=self.account.access_token_key,
                access_token_secret=self.account.access_token_secret,
            )

        if self.account.type == 'instagram':
            return instagram.InstagramAPI(
                client_id=self.account.client_id,
                client_secret=self.account.client_secret,
            )

        raise NotImplementedError('No API definition found for %s' % self.account.type)

    def normalize_posts(self, results):
        """
            Take results from a given search and turn them into something predicatable
            we can use elsewhere reliably
        """
        if self.account.type == 'twitter':
            return [TwitterPost(p) for p in results]
        else:
            return [InstagramPost(p) for p in results]

    def search(self, term, count=100):
        """
            Perform a search depending on the service used with the given term
            and counts
        """

        api = self.get_api()

        if self.account.type == 'instagram':
            # Instagram tagged media
            results, url = api.tag_recent_media(count, None, term)
        else:
            # Twitter general stream for search
            results = api.GetSearch(term=term, count=count, result_type='recent')

        return self.normalize_posts(results)

