from sanic.response import json
from .system_io import get_license


async def get_license_or_404(license_name, license_list):
    if license_name not in license_list:
        return json({}, status=404)
    return await get_license(license_name)


def get_searched_data(raw_args, license_list):
    if "search" in raw_args:
        return [item for item in license_list if raw_args["search"] in item]
    return license_list


def get_paginated_data(raw_args, license_list):
    if "page" in raw_args and "page_size" in raw_args:
        page_size = int(raw_args["page_size"]) if int(raw_args["page_size"]) > 0 else 0
        page = int(raw_args["page"]) if int(raw_args["page_size"]) > 0 else 0
        return (
            license_list[page * page_size: (page + 1) * page_size],
            True if license_list[(page + 1) * page_size: (page + 2) * page_size] else False,
            True if license_list[(page - 1) * page_size: page * page_size] else False
        )
    return license_list, None, None
