
CRAWN_SPOJ = '/crawnspojstart'

WORKER_QUEUE_URL = '/urldownloader'

PROBLEM_NAME = '[A-Z0-9]+'
USER_NAME = '[a-z0-9_]+'

#pages of interest
PROBLENS_PAGE_PATTERN = '.*/problems/' + PROBLEM_NAME + '/$'
USERS_PAGE_PATTERN = '.*/users/' + USER_NAME + '/$'
SUBMISSIONS_PAGE_PATTERN = '.*/status/' + USER_NAME + '/signedlist/$'

#default recommender in mencache
DEFAULT_RECOMMENDER = 'defaultRecommender'
