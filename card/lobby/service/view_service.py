import logging

class ViewService(object):

    def __init__(self, service_repositories, activity_repository):
        self.service_repositories = service_repositories
        self.activity_repository = activity_repository
        self.trans_logger = logging.getLogger('trans_log')
