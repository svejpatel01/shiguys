"""Build static HTML site from directory of HTML templates and plain files."""

import json
from pathlib import Path
from distutils.dir_util import copy_tree
import jinja2
import click


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('--output', '-o', default="", type=click.Path(writable=True),
              help='Output directory.')
@click.option('--verbose', '-v', is_flag=True, help='Print more output.')
def main(input_dir, output, verbose):
    """Templated static website generator."""
    # Creating OUTPUT and INPUT_DIR path objects.
    if output == "":
        output = Path(input_dir) / 'html'  # default output
    else:
        output = Path(output)
    input_dir = Path(input_dir)

    # Creating OUTPUT directory
    Path.mkdir(output, parents=False, exist_ok=True)

    # Copy STATIC directory over if it exists
    if Path(input_dir / 'static').exists():
        static_dir = Path(input_dir / 'static')
        copy_tree(str(static_dir), str(output))
        if verbose:
            print("Copied", static_dir, "->", output)

    # Getting context data from config.json file in the INPUT_DIR
    get_data = input_dir / 'config.json'
    with get_data.open() as j:
        data = json.load(j)

    for index in data:
        url = index['url']
        url = url.lstrip('/')

        # Creating index.html file in OUTPUT directory
        temp = output / Path(url)
        Path.mkdir(temp, parents=True, exist_ok=True)
        Path(temp / 'index.html').touch()

        # Getting data[0]['template'] template from
        # {INPUT_DIR}/templates/ directory
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(input_dir / 'templates'),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            )
        template = template_env.get_template(index['template'])

        # Opening the {OUTPUT}/index.html created earlier so we can write to it
        out = output / url / 'index.html'
        # s = template.render(words = data[0]['context']['words'])
        final_output = template.render(index['context'])
        out.write_text(final_output)
        if verbose:
            print("Rendered", index['template'], "->", out)


if __name__ == "__main__":
    main()
