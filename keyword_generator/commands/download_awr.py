import click
from keyword_generator.commands.base import cli, check_parameter_in_config_file, set_parameter_value, \
    get_awr_cloud_project
from keyword_generator.csv import save_csv

__author__ = 'fabrice'

@cli.command(name='download-awr', help='Download keyphrases from AWR cloud into a file (AWR Cloud keyword export)')
@click.argument('output', default='awr_kw_export.csv')
@click.option('--username', "-u", callback=check_parameter_in_config_file)
@click.option('--password', callback=check_parameter_in_config_file)
@click.option('--project-id', "-p")
@click.pass_context
def download_awr(ctx, output, username, password, project_id):

    set_parameter_value(ctx, "awr-kw-export-file", output)

    click.echo("running 'kw-dl-awr' command with:")
    click.echo("awr_kw_export_file = " + output)


    awr_cloud_project = get_awr_cloud_project(password, username, project_id)
    awr_cloud_project.fetch_keywords()
    rows = [["", "", kw] for kw in awr_cloud_project._keywords]
    save_csv(output, rows, ["","","keyphrases"])
    click.echo("Wrote file '%s'" % output)
