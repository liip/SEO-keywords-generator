import click
from base import cli, get_awr_cloud_project, set_parameter_value
from keyword_generator import csv
from keyword_generator.csv import save_csv

__author__ = 'fabrice'

@cli.command(name='download-awr', help='Download keyphrases from AWR cloud into a file (AWR Cloud keyword export)')
@click.argument('output', default='awr_kw_export.csv')
@click.option('--username', "-u", prompt=True)
@click.option('--project-id', "-p")
@click.password_option(confirmation_prompt=False)
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