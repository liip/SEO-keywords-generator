import click
from keyword_generator.awrcloud.AwrCloud import AwrCloud


@click.group(chain=True)
#@click.command()
@click.pass_context
def cli(ctx):
    #settings = Settings(config)
    ctx.obj = {}
    #ctx.obj['settings'] = settings
    #ctx.obj['view'] = TtyUi()
    #ctx.obj['projects_db'] = ProjectsDb(os.path.expanduser(taxi_dir))

def get_parameter_value(ctx, name, value):
    if "data" in ctx.obj and name in ctx.obj["data"]:
        return ctx.obj["data"][name]
    return value

def set_parameter_value(ctx, name, value):
    if "data" not in ctx.obj:
        ctx.obj["data"] = {}
    ctx.obj["data"][name] = value

def get_awr_cloud_project(password, username, project_id=None):
    awr_cloud = AwrCloud(username, password, dry_run=False, debug=False)
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
