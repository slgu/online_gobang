import threading
from django.core.cache import get_cache
import logging
VALIDATION_TIME = 5 * 60
REALTIME_MAXDELTA = 24 * 60 * 60 * 30


#cache
validation_cache = get_cache('default')
play_info_cache = get_cache('play_info')
online_people = set()


#log
gobang_logger = logging.getLogger('gobang')