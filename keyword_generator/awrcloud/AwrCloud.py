import logging

from AwrCloudApi import AwrCloudAPI
from keyword_generator.awrcloud import pages_parser
from keyword_generator.awrcloud.AwrCloudProject import AwrCloudProject

__author__ = 'fabrice'

class AwrCloud:

    def __init__(self, username, password, dry_run=False, debug=False):
        self._awr_cloud_api = AwrCloudAPI(debug, dry_run, username, password)
        if debug:
            self.enable_lib_debugs()

    def enable_lib_debugs(self):
        try:
            import http.client as http_client
        except ImportError:
            # Python 2
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1

        # initialize logging, otherwise debug output cannot be seen
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def get_projects(self):
        projects_page = self._awr_cloud_api.get_projects_page()
        return pages_parser.parse_projects_from_html(projects_page.text)

    def get_project(self, project_id):
        return AwrCloudProject(project_id, self._awr_cloud_api)