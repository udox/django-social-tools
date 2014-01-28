import twitter
import instagram

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

    def search(self, term, result_type='recent', count=100):
        api = self.get_api()

        if self.account.type == 'twitter':
            return api.GetSearch(term=term, count=count, result_type=result_type)
        else:
            return []


