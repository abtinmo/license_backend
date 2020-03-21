from sanic import Sanic
from sanic.response import json

from utils import (
    get_license_list, get_license_or_404, prepare_data,
    get_paginated_data, get_searched_data
)


prepare_data()
license_list = get_license_list()

app = Sanic()


@app.route("/license/", methods=["GET"])
async def list_result(request):
    """
        query params are [search, page >= 0, page_size >=0]
    """
    searched_list = get_searched_data(request.raw_args, license_list)
    paginated_list, is_next_query, is_previous_query = get_paginated_data(
        request.raw_args,
        searched_list
    )
    return json(
        {
            "data": {
                "next": is_next_query,
                "previous": is_previous_query,
                "count": len(searched_list),
                "results": paginated_list
            }
        }
    )


@app.route("/license/<license_name:string>/", methods=["GET"])
async def detail_result(request, license_name):
    return await get_license_or_404(license_name, license_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
