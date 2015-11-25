from keyword_generator.awrcloud.awr_items import AwrKeyword, AwrGroup

__author__ = 'fabrice'
from bs4 import BeautifulSoup

def parse_keyword_id(javascript):
    if not ("(" in javascript and ")" in javascript):
        raise Exception("Malformed javascript to parse id : " + javascript)
    index_open = javascript.index("(")
    index_close = javascript.index(")")
    if index_open > index_close:
        raise Exception("Malformed javascript parenthesis to parse id : " + javascript)
    return javascript[index_open+1:index_close]

def parse_keywords_from_html(content):
    soup = BeautifulSoup(content)
    table = soup.find(id="keywords_table")
    if table is None:
        return []
    rows = table.tbody.find_all("tr")
    keywords = []
    for row in rows:
        cells = row.find_all("td")
        for cell in cells:
            if cell.has_attr("onclick"):
                id = parse_keyword_id(cell["onclick"])
                keywords.append(AwrKeyword(cell.text.strip(), id))
                break
    return keywords

def parse_total_keywords(content):
    soup = BeautifulSoup(content)
    pagination = soup.find_all(class_="table-pagination")[0]

    of_ = " of "
    if of_ in pagination.text:
        return int(pagination.text[pagination.text.index(of_)+4:].strip())
    elif "total keywords" in pagination.text:
        txt = pagination.text.strip()
        return int(txt.split(" ")[0])
    raise Exception("wrong format for pagination tag : " + pagination.text)



def parse_groups_from_html(content):
    soup = BeautifulSoup(content)
    tbody = soup.find(id="current_groups")
    if tbody is None:
        return []
    rows = tbody.find_all("tr")
    groups = []
    for row in rows:
        cell = row.find_all("td")[1]
        links = cell.find_all("a")
        name = links[0].text.strip()
        id = cell.input["value"]
        groups.append(AwrGroup(name, id))
    return groups

def parse_projects_from_html(content):
    def parse_project(project_row):
        cells = project_row.find_all("td")
        project_id = parse_keyword_id(cells[0]["onclick"])
        project_name = cells[1].a["title"][4:-4]

        return (project_id, project_name)

    soup = BeautifulSoup(content)
    div_table = soup.find_all(class_="table-responsive")
    if (len(div_table)==0):
        raise Exception("Error during page parsing. Verify if you got correctly connected")
    div_table = div_table[0]
    projects_rows = div_table.table.tbody.find_all("tr")
    return [parse_project(row) for row in projects_rows]
