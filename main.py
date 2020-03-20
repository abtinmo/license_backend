import os
import subprocess

import aiofiles
from sanic import Sanic
from sanic.response import json
import ujson


if not os.path.exists("./license-list-data"):
    bash_command = "git clone https://github.com/spdx/license-list-data"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
else:
    bash_command = "git -C license-list-data pull"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

path = os.getcwd()
license_list = [
    item.replace(".json", "")
    for item in os.listdir("./license-list-data/json/details/")
    ]
license_list.sort()

app = Sanic()


@app.route("/license", methods=["GET"])
async def list_result(request):
    return json(
        {
            "data": {
                "count": len(license_list),
                "results": license_list
            }
        }
    )


@app.route("/license/<license_name:string>/", methods=["GET"])
async def detail_result(request, license_name):
    if license_name not in license_list:
        return json({}, status=404)
    async with aiofiles.open(
        "./license-list-data/json/details/{1}.json".format(license_name),
        "r"
    ) as f:
        data = ujson.loads(await f.read())
    return json(
        {
            "data": data
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
