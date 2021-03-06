from django.conf import settings
import os

AWS_ENABLED = getattr(settings, 'AWS_ENABLED', False)
BASE_DIR = getattr(settings, 'BASE_DIR')
MEDIA_URL = settings.MEDIA_URL if settings.MEDIA_URL else '/media/'  # settings.MEDIA_URL if settings.MEDIA_URL else '/media/'
MEDIA_ROOT = settings.MEDIA_ROOT if settings.MEDIA_ROOT else os.path.join(BASE_DIR + '/media/')  # settings.MEDIA_ROOT if settings.MEDIA_ROOT else os.path.join(BASE_DIR + '/media/')

DISQUS_SHORTNAME = getattr(settings, 'DISQUS_SHORTNAME', '')

BLOG_TITLE = "Kaustav Banerjee"
BLOG_DESCRIPTION = "Travel , Music , Videos and Geeky Fun"
BLOG_KEYWORDS = "travel , music , video , song , movie , geek , comics , anime"
BLOG_AUTHOR = "kauxtav1996"
STRIPE_SECRET_KEY = 'sk_test_j8ULflzHxbsXvSMaEHAGXFVl003H8o86RT'
STRIPE_PUBLISHABLE_KEY = 'pk_test_ivFuxlMPRIwblreWKSoYKT8f00TsVpGygT'