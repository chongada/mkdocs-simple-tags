# --------------------------------------------
# Main part of the plugin
#
# JL Diaz (c) 2019
# Tai Vo (c) 2021
# MIT License
# --------------------------------------------
from collections import defaultdict
from pathlib import Path
import jinja2
import os
from mkdocs.structure.files import File
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from mkdocs.utils import meta as meta_util, get_markdown_title


class SimpleTagsPlugin(BasePlugin):
    """
    Creates "tags.md" file containing a list of the pages grouped by simple_tags

    It uses the info in the YAML metadata of each page, for the pages which
    provide a "simple_tags" keyword (whose value is a list of strings)
    """

    config_scheme = (
        ('tags_filename', Type(str, default='tags.md')),
        ('tags_folder', Type(str, default='_aux')),
        ('tags_template', Type(str)),
    )

    def __init__(self):
        self.metadata = []
        self.tags_filename = "tags.md"
        self.tags_folder = "_aux"
        self.tags_template = None

    # def on_nav(self, nav, config, files):
    #     # nav.items.insert(1, nav.items.pop(-1))
    #     pass

    def on_config(self, config):
        # Re assign the options
        self.tags_filename = Path(self.config.get("tags_filename") or self.tags_filename)
        self.tags_folder = Path(self.config.get("tags_folder") or self.tags_folder)
        # Make sure that the simple_tags folder is absolute, and exists
        if not self.tags_folder.is_absolute():
            self.tags_folder = Path(config["docs_dir"]) / ".." / self.tags_folder
        if not self.tags_folder.exists():
            self.tags_folder.mkdir(parents=True)

        if self.config.get("tags_template"):
            self.tags_template = Path(self.config.get("tags_template"))

    def on_files(self, files, config):
        # Scan the list of files to extract simple_tags from meta
        for f in files:
            _, extension = os.path.splitext(f.src_path)
            if extension not in (".md", ".markdown"):
                continue
            self.metadata.append(get_metadata(f.src_path, config["docs_dir"]))

        # Create the new "Tags" index file
        self.generate_tags_file()

        # New file to add to the build
        newfile = File(
            path=str(self.tags_filename),
            src_dir=str(self.tags_folder),
            dest_dir=config["site_dir"],
            use_directory_urls=True
        )
        files.append(newfile)

    def generate_tags_page(self, data):
        if self.tags_template is None:
            templ_path = Path(__file__).parent / Path("templates")
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(templ_path))
                )
            templ = environment.get_template("tags.md.template")
        else:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(searchpath=str(self.tags_template.parent))
            )
            templ = environment.get_template(str(self.tags_template.name))
        output_text = templ.render(
                tags=sorted(data.items(), key=lambda t: t[0].lower()),
        )
        return output_text

    def generate_tags_file(self):
        sorted_meta = sorted(self.metadata, key=lambda e: e.get("year", 5000) if e else 0)
        tag_dict = defaultdict(list)
        for e in sorted_meta:
            if not e:
                continue
            tags = e.get("tags", [])
            if tags is not None:
                for tag in tags:
                    tag_dict[tag].append(e)

        t = self.generate_tags_page(tag_dict)

        with open(str(self.tags_folder / self.tags_filename), "w") as f:
            f.write(t)


#
# Helper functions
#

def get_metadata(name, path):
    filename = Path(path) / Path(name)
    with open(filename, 'r', encoding='utf-8-sig', errors='strict') as f:
        source = f.read()
        md_content, meta = meta_util.get_data(source)

        if meta:
            if 'title' not in meta:
                meta['title'] = get_markdown_title(md_content)
            meta['filename'] = name
            return meta
