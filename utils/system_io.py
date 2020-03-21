import os
import subprocess

import aiofiles
import ujson
from sanic.response import json


def get_license_list():
    return sorted(
        [
            item.replace(".json", "")
            for item in os.listdir("./license-list-data/json/details/")
        ]
    )


def prepare_data():
    if not os.path.exists("./license-list-data"):
        run_bash_sub_prosses("git clone https://github.com/spdx/license-list-data")
    else:
        run_bash_sub_prosses("git -C license-list-data pull")


def run_bash_sub_prosses(bash_command):
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    return process.communicate()


async def get_license(license_name):
    async with aiofiles.open(
        "./license-list-data/json/details/{0}.json".format(license_name),
        "r"
    ) as f:
        return json(ujson.loads(await f.read()))
