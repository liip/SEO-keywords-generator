__author__ = 'fabrice'
import pprint
import requests

browser_headers={
    "Origin" : "https://www.awrcloud.com",
    "Accept-Encoding" : "gzip, deflate",
    "Accept-Language" : "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
    "Upgrade-Insecure-Requests" : 1,
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control" : "max-age=0",
    "Referer" : "https://www.awrcloud.com/login.php",
    "Connection" : "keep-alive",
    "X-Requested-With":"XMLHttpRequest",
}

connection_data = {
    "action" : "login",
    "remember_me" : "on",
    "commit" : "",
    "token" : "",
    "invite" : "",
    "autoredir" : "",
    "redirect" : "",
    "redirect_action" : ""
}

# default_cookies = {
#     "perpage_kw" : "1000"
# }

login_url = "https://www.awrcloud.com/index.php"
awr_cloud_url = "https://www.awrcloud.com/"

def pretty_print(type, headers):
    print ("*" + type.upper() + ": ")
    pprint.pprint(headers)
    print("\n")

def print_request_info(info_name, url, response, data=None, print_text=False):
    print ("**** %s on url '%s':" % (info_name.upper(), url))
    pretty_print("request", response.request.headers._store)
    pretty_print("response", response.headers._store)
    if print_text:
        print ("*RESPONSE TEXT: ")
        print(response.text)
    pretty_print("cookies", response.cookies._cookies)
    if data is not None:
        pretty_print("data", data)

class AwrCloudAPI:

    def __init__(self, debug, dry_run, username, password):
        self._dry_run = dry_run
        self._session = requests.session()
        self._debug = debug
        # self._session.cookies.update(default_cookies)
        print ("Connecting to AWRCloud...")
        authentication_data = dict(connection_data)
        authentication_data["email"] = username
        authentication_data["password"] = password
        response = self._session.post(login_url, authentication_data, headers=browser_headers)
        print ("Connected to AWRCloud")
        if self._debug:
            print_request_info("connexion", login_url, response)

    def assign_keyword_to_new_group(self, keyword_ids, project_id, group_name):
        data = {
            "items" : ",".join(keyword_ids),
            "project_id" : project_id,
            "group_name" : group_name
        }
        return self.post_project_action("projects", "assign_keywords_new_group", data)

    def add_keywords(self, project_id, keyphrases):
        data = {
            "action" : "perform_addkeywords",
            "fromkwsmanage":1,
            "project_id" :project_id,
            "updatefrequency":"",
            "new_project" : "",
            "keywords" : "\r\n".join(keyphrases),#"%0D%0A".join([kp.strip().replace(" ", "+") for kp in keyphrases]),
            "group_id" : -3,
            "new_group" : ""
        }
        return self.post_project_action("projects", None, data)

    def assign_keyword_to_existing_group(self, keyword_ids, project_id, group_id):
        data = {
            "items" : ",".join(keyword_ids),
            "project_id" : project_id,
            "items_groups" : group_id
        }
        return self.post_project_action("projects", "assign_keywords_to_groups", data)

    def delete_groups(self, project_id, group_ids):
        data = {
            "items" : ",".join(group_ids),
            "project_id" : project_id
        }
        return self.post_project_action("keyword_groups", "deleteGroups", data)

    def get_keywords_page(self, project_id, perpage, offset):
        params = {
            "action" : "manageproject",
            "activetab" : "keywords",
            "sorttype":"keywordrank",
            "sortdir":"asc",
            "project_id" : project_id,
            "perpage" : str(perpage),
            "offset":str(offset)
        }
        response = self.get_page("projects", params)
        return response

    def get_projects_page(self):
        response = self.get_page("projects")
        return response


    def get_groups_page(self, project_id):
        params = {
            "project_id" : project_id,
        }

        response = self.get_page("keyword_groups", params)
        return response

    def post_project_action(self, page, action, data):

        params = {
            "action" : action,
        } if action is not None else None
        url = awr_cloud_url + "/" + page + ".php"

        if self._dry_run:
            print ("fake posting on url '%s' with params '%s' and data '%s'" % (url, params, data))
            return FakeResponse()

        response = self._session.post(url, data, params=params, headers=browser_headers)
        if self._debug:
            print_request_info("post %s" % action, url, response, data)
        return response


    def get_page(self, page, params={}):
        url = awr_cloud_url + "/" + page + ".php"
        response = self._session.get(url, params=params, headers=browser_headers)
        if self._debug:
            print("GET on page %s" % url + "?"+"&".join([k+"="+v for k, v in params.iteritems()]) if len(params)!=0 else "")
            print_request_info("get %s" % page, url, response)
        return response

class FakeResponse:
    text="fake response"