from keyword_generator.awrcloud import pages_parser

__author__ = 'fabrice'

class AwrCloudProject:

    def __init__(self, project_id, awr_cloud_connector):
        self._project_id = project_id
        self._awr_cloud_connector = awr_cloud_connector

    def determine_unused_groups(self, used_groups_names):
        return [group for group_name, group in iter(self._groups.items()) if group_name not in used_groups_names]

    def delete_groups(self, groups):
        self._awr_cloud_connector.delete_groups(self._project_id, [group.id for group in groups])

    def assign_to_group(self, keywords, group):
        kwObjs = []
        for keyword in keywords:
            if keyword not in self._keywords:
                raise Exception("keyword '%s' doesn't exists" % keyword)
            kwObjs.append(self._keywords[keyword])

        kwIds = [kwObj.id for kwObj in kwObjs]
        if group in self._groups:
            groupObj = self._groups[group]
            response = self._awr_cloud_connector.assign_keyword_to_existing_group(kwIds, self._project_id, groupObj.id)
            print ("%s keyphrases to existing group '%s'" % (len(kwObjs), groupObj))
        else:
            response = self._awr_cloud_connector.assign_keyword_to_new_group(kwIds, self._project_id, group)
            print ("%s keyphrases assigned to new group '%s'" % (len(kwObjs), group))
        print ("response : " + response.text)

    def add_keywords(self, keyphrases):
        self._awr_cloud_connector.add_keywords(self._project_id, keyphrases)

    def update_state(self):
        print ("Fetching project state from AWRCloud")
        self.fetch_keywords()
        self.fetch_groups()

    def fetch_keywords(self):
        def html_to_keyword_dict(html):
            keywords = pages_parser.parse_keywords_from_html(html)
            return {
                keyword.name : keyword
                    for keyword in keywords
            }

        perpage = 1000
        keywords_page = self._awr_cloud_connector.get_keywords_page(self._project_id, perpage, 0)
        total_keywords = pages_parser.parse_total_keywords(keywords_page.text)
        print ("Fetching keywords...")
        print ("Retrieved %s keywords" % total_keywords)
        self._keywords = html_to_keyword_dict(keywords_page.text)
        for offset in range (perpage, total_keywords, perpage):
            print ("Fetching remaining keywords from " + str(offset))
            keywords_page = self._awr_cloud_connector.get_keywords_page(self._project_id, perpage, offset)
            self._keywords.update(html_to_keyword_dict(keywords_page.text))

    def fetch_groups(self):
        print ("Fetching groups...")
        groups_page = self._awr_cloud_connector.get_groups_page(self._project_id)
        groups = pages_parser.parse_groups_from_html(groups_page.text)
        self._groups = {
            group.name : group
                for group in groups
        }
        print ("Fetched %s groups" % len(self._groups))
