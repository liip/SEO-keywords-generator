from keyword_generator.awrcloud.awr_items import AwrKeyword, AwrGroup

__author__ = 'fabrice'
from bs4 import BeautifulSoup

def read_html(content):
    return BeautifulSoup(content, 'html.parser')

def parse_id(javascript):
    if not ("(" in javascript and ")" in javascript):
        raise Exception("Malformed javascript to parse id : " + javascript)
    index_open = javascript.index("(")
    index_close = javascript.index(")")
    if index_open > index_close:
        raise Exception("Malformed javascript parenthesis to parse id : " + javascript)
    return javascript[index_open+1:index_close]

def parse_keywords_from_html(content):
    soup = read_html(content)
    table = soup.find(id="keywords_table")
    if table is None:
        return []
    rows = table.tbody.find_all("tr")
    keywords = []
    for row in rows:
        cells = row.find_all("td")
        id = cells[1].select("input")[0].get("value")
        word = cells[2].text.strip()
        keywords.append(AwrKeyword(word, id))
    return keywords

def parse_total_keywords(content):
    soup = read_html(content)
    pagination = soup.find_all(class_="table-pagination")[0]

    of_ = " of "
    if of_ in pagination.text:
        return int(pagination.text[pagination.text.index(of_)+4:].strip())
    elif "total keywords" in pagination.text:
        txt = pagination.text.strip()
        return int(txt.split(" ")[0])
    raise Exception("wrong format for pagination tag : " + pagination.text)



def parse_groups_from_html(content):
    soup = read_html(content)
    tbody = soup.find(id="current_groups")
    if tbody is None:
        return []
    rows = tbody.find_all("tr")
    groups = []
    for row in rows:
        if (row.get("class") == "group-row"):
            cells = row.find_all("td")
            name = cells[2].text.strip()
            id = cells[1].input["value"]
            groups.append(AwrGroup(name, id))
    return groups

def parse_projects_from_html(content):
    def parse_project(project_row):
        cells = project_row.find_all("td")
        project_id = parse_id(cells[0]["onclick"])
        project_name = cells[1].a["title"][4:-4]

        return (project_id, project_name)

    soup = read_html(content)
    div_table = soup.find_all(class_="table-responsive")
    if (len(div_table)==0):
        raise Exception("Error during page parsing. Probably a wrong username and password")
    div_table = div_table[0]
    projects_rows = div_table.table.tbody.find_all("tr")
    return [parse_project(row) for row in projects_rows]
