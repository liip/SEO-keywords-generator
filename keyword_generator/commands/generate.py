import click
from keyword_generator.commands.base import cli, set_parameter_value

from keyword_generator.kw_generator import generate_combinations, save_combinations

__author__ = 'fabrice'

@cli.command(help="Generate keywords from an input directory")
@click.argument('input-dir', type=click.Path(exists=True), default=".")
@click.option('--patterns-file', '-t', default="patterns.csv")
@click.option('--output', '-o', default='keywords.csv', help="file to output (default = 'keywords.csv')")
#@click.help_option()
@click.pass_context
def generate(ctx, input_dir, patterns_file, output):

    set_parameter_value(ctx, "gen-kw-file", output)

    click.echo ("running 'generate' command with:")
    click.echo ("input_dir = " + input_dir)
    click.echo ("ouput_file = " + output)
    combinations = generate_combinations(input_dir, patterns_file)
    click.echo("Writing file '%s'" % output)
    save_combinations(output, combinations)
