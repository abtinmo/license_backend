from sanic.response import json
from .system_io import get_license


async def get_license_or_404(license_name, license_list):
    if license_name not in license_list:
        return json({}, status=404)
    return await get_license(license_name)
