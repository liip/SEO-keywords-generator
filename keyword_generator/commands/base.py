from configparser import ConfigParser, NoSectionError, NoOptionError
import click

from keyword_generator.awrcloud.AwrCloud import AwrCloud


@click.group(chain=True)
#@click.command()
@click.option('--debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug


def get_parameter_value(ctx, name, value):
    if "data" in ctx.obj and name in ctx.obj["data"]:
        return ctx.obj["data"][name]
    return value

def set_parameter_value(ctx, name, value):
    if "data" not in ctx.obj:
        ctx.obj["data"] = {}
    ctx.obj["data"][name] = value

def check_parameter_in_config_file(ctx, name, value):
    if value is not None:
        return value
    def get_param_value_in_config(param):
        from os import path
        home = path.expanduser("~")
        filePath = path.join(home, ".kwgen/config.ini")
        if not path.isfile(filePath):
            return value
        result = None
        config = ConfigParser()
        config.read(filePath)
        try:
            result = config.get('authentication', param)
        except (NoSectionError, NoOptionError) as e:
            return value
        return result

    p_name = name.name
    value = get_param_value_in_config(p_name)
    if value is None:
        raise Exception("Parameter '%s' is mandatory" % p_name)
    click.echo("Using parameter '%s' in config file" % p_name)
    return value

def get_awr_cloud_project(password, username, project_id=None, debug=False):
    awr_cloud = AwrCloud(username, password, dry_run=False, debug=debug)
    projects = awr_cloud.get_projects()
    if project_id is None:
        selected_project = select_project(projects)
    else:
        selected_project = None
        for project in projects:
            if project[0]==project_id:
                selected_project = project
        if project==None:
            click.echo("Project with id '%s' doesn't exist")
            exit(1)
    click.echo("selected project : " + repr(selected_project))
    awr_cloud_project = awr_cloud.get_project(selected_project[0])
    return awr_cloud_project

def select_project(projects):
    while 1:
        value = click.prompt("Chose amont the following projects:\n    %s\n" % "\n    ".join(
            [
                str(project_item[0]) + " - " + project_item[1][1] for project_item in enumerate(projects)
                ]
        ), type=int)
        if value >= len(projects):
            click.echo("Selected value is out of range")
            continue
        break
    selected_project = projects[value]
    return selected_project
