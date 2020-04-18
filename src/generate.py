#!/usr/bin/env python3
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
from distutils.dir_util import copy_tree
import yaml
from pathlib import Path


def main(args):
    is_release = "release" in args

    sections = load_yaml("./structure.yml")["sections"]
    authorities = load_yaml("./authorities.yml")["authorities"]

    for section in sections:
        for column in section["columns"]:
            for entry in column:
                entry["authorities"] = [a for a in authorities if set(
                    a["tags"]).issuperset(set(entry["tags"]))]

    env = Environment(
        loader=PackageLoader('generate', './templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    Path("../out").mkdir(parents=True, exist_ok=True)
    (env.get_template('home.html')
     .stream(release=is_release, sections=sections)
     .dump('../out/index.html'))

    Path("../out/law").mkdir(parents=True, exist_ok=True)
    (env.get_template('law.html')
     .stream(release=is_release, sections=sections)
     .dump('../out/law/index.html'))

    copy_tree("./static", "../out")


def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


if __name__ == "__main__":
    main(sys.argv[1:])
