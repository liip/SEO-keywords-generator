import click
from keyword_generator import csv
from keyword_generator.commands.base import cli, get_parameter_value

__author__ = 'fabrice'


@cli.command(name='compare-awr', help='Compare generated keywords with AWR Cloud keyword export')
@click.argument('awr-kw-export-file', type=click.Path(exists=True), default='awr_kw_export.csv')
@click.argument('gen-kw-file', type=click.Path(exists=True), default='keywords.csv')
@click.pass_context
def compare_awr(ctx, awr_kw_export_file, gen_kw_file):

    awr_kw_export_file = get_parameter_value(ctx, "awr-kw-export-file", awr_kw_export_file)
    gen_kw_file = get_parameter_value(ctx, "gen-kw-file", gen_kw_file)

    click.echo("running 'compare-awr' command with:")
    click.echo("awr_kw_export_file = " + awr_kw_export_file)
    click.echo("gen-kw-file = " + gen_kw_file)

    def first_not_in_second(lines_first, lines_second):
        return [line for line in lines_first if line not in lines_second]

    def list_str(keywords):
        return "[\n" + ",   \n".join(keywords) + "\n]" if len(keywords)!=0 else "[(empty)]"

    gen_keywords = csv.read_csv_column_distinct(gen_kw_file, 0)
    awr_keywords = csv.read_csv_column_distinct(awr_kw_export_file, 2, quote_char='"')

    click.echo("")
    click.echo("Keywords only present in generated keywords :")
    click.echo(list_str(first_not_in_second(gen_keywords, awr_keywords)))

    click.echo("")
    click.echo("Keywords only present in AWR Cloud keywords :")
    click.echo(list_str(first_not_in_second(awr_keywords, gen_keywords)))
    click.echo("")