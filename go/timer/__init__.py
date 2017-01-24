import gevent
from gevent.hub import get_hub

import go.error
import go.logging

def new_timer(delay, timeout_cb, *args):
    timer = get_hub().loop.timer(delay, ref=False)
    def timeout_callback():
        logger = go.logging.get_logger('timer')
        try:
            timeout_cb(*args)
        except go.error.Warning, ex:
            logger.warning(ex)
        except go.error.Error, ex:
            logger.error(ex)
    timer.start(timeout_callback)
    return timer
