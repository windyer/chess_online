from redis_sessions import session
from card.core.conf import settings

import go.containers
from card.core.util.mutex import Mutex

class SessionStore(session.SessionStore):

    def _save_session_map(self, user_id):
        mapping_key = settings.SESSION_MAPPING_KEY.format(user_id=user_id)
        old_session = self.server.get(mapping_key)
        new_session = self._get_session_key()
        if old_session and old_session != new_session:
            self.server.delete(
                settings.SESSION_REDIS_PREFIX + ':' + old_session
            )
        expire_age = self.get_expiry_age()
        self.server.setex(mapping_key, expire_age, new_session)

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create)

        user_id = self._session.get('_auth_user_id', 0)
        checked_else_logon = self._session.get('checked_else_logon', False)
        if user_id and not checked_else_logon:
            timeout = settings.TIMEOUT.lock_timeout
            mutex = Mutex("Session:Store" + str(user_id), timeout, go.containers.get_client())
            try:
                mutex.lock()
                self._session["checked_else_logon"] = True
                self._save_session_map(user_id)
            finally:
                mutex.unlock()
