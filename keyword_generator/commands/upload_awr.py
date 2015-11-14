from keyword_generator import csv
from keyword_generator.commands.base import get_awr_cloud_project, cli

__author__ = 'fabrice'

import click



@cli.command(name='upload-awr', help='Upload keyphrases and groups to AWR Cloud using generated keyword file')
@click.argument('gen-kw-file', type=click.Path(exists=True), default='keywords.csv')
@click.option('--username', "-u", prompt=True)
@click.option('--project-id', "-p")
@click.password_option(confirmation_prompt=False)
def upload_awr(gen_kw_file, username, password, project_id):
    click.echo("running 'assign_groups' command with:")
    click.echo("gen-kw-file = " + gen_kw_file)

    # choose AWR cloud project
    awr_cloud_project = get_awr_cloud_project(password, username, project_id)

    # read generated keyphrases file
    keyphrases, assignations = read_assignations(gen_kw_file)

    # upload keyphrases
    confirm_continue("You are going to add %s keyphrases in AWR Cloud. Are you sure ?" % len(keyphrases))
    awr_cloud_project.add_keywords(keyphrases)
    awr_cloud_project.fetch_keywords()

    # assign groups in AWR cloud
    confirm_continue("You are going to assign %s groups in AWR Cloud. Are you sure ?" % len(assignations))

    assigned_groups = set()
    awr_cloud_project.fetch_groups()
    for group, keyphrases in assignations.iteritems():
        awr_cloud_project.assign_to_group(keyphrases, group)
        assigned_groups.add(group)

    # delete unused groups
    awr_cloud_project.fetch_groups()
    unused_groups = awr_cloud_project.determine_unused_groups(assigned_groups)

    group_list_display = ",\n".join(
            [
                "- " + group.name for group in unused_groups
            ]
        )

    if (len(unused_groups)!=0):
        confirm_continue("After assignations, the following %s groups remain unused:\n%s\nDo you want to delete them from AWR Cloud ?" % (len(unused_groups), group_list_display))
        awr_cloud_project.delete_groups(unused_groups)

    click.echo("Successfully imported keywords and groups in AWR Cloud")

def confirm_continue(message):
    answer = click.prompt(message + " (y/n)", type=str).lower()

    if answer!='y':
        click.echo("Quitting")
        exit(0)

"""
    will return
    {group : [keyphrase1, keyphrase2, ...]}
"""
def read_assignations(gen_kw_file):
    assignation = {}
    rows = csv.get_rows(gen_kw_file)
    keyphrases = set()
    def assign(kp, group):
        if group not in assignation:
            assignation[group] = [kp]
        else:
            assignation[group].append(kp)

    for generated_keyphrase in rows:
        kp = generated_keyphrase[0]
        keyphrases.add(kp)

        for lang in generated_keyphrase[1].split("|"):
            assign(kp, "lang_" + lang)
        topics = generated_keyphrase[2].split("|")
        for topic in topics:
            assign(kp, "topic_" + topic)
        pattern = "pattern_" + "-".join(topics)
        assign(kp, pattern)

    return (keyphrases, assignation)
