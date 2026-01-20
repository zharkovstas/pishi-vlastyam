#!/usr/bin/env python3
from jinja2 import Environment, PackageLoader, select_autoescape
import os
import shutil
import stat
import sys
import yaml
from pathlib import Path


def main(args):
    is_release = "release" in args

    sections = load_yaml("./structure.yml")["sections"]
    authorities = load_yaml("./authorities.yml")["authorities"]

    for section in sections:
        for column in section["columns"]:
            for entry in column:
                entry["authorities"] = [
                    a
                    for a in authorities
                    if set(a["tags"]).issuperset(set(entry["tags"]))
                ]

    env = Environment(
        loader=PackageLoader("generate", "./templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    Path("../out").mkdir(parents=True, exist_ok=True)
    (
        env.get_template("home.html")
        .stream(release=is_release, sections=sections)
        .dump("../out/index.html")
    )

    copytree("./static", "../out")


def load_yaml(path):
    with open(path, "r") as stream:
        return yaml.safe_load(stream)


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)

    if ignore:
        exclude = ignore(src, lst)
        lst = [x for x in lst if x not in exclude]

    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)

            os.symlink(os.readlink(s), d)

            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass  # lchmod not available

        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


if __name__ == "__main__":
    main(sys.argv[1:])
