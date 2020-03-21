from sanic import Sanic
from sanic.response import json

from utils import (
    get_license_list, get_license_or_404, prepare_data
)


prepare_data()
license_list = get_license_list()

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
    return await get_license_or_404(license_name, license_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
