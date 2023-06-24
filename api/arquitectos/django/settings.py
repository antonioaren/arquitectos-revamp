from pathlib import Path
import os
from importlib import metadata
from model_w.env_manager import EnvManager
from model_w.preset.django import ModelWDjango

DEBUG = None
REST_FRAMEWORK = {}
BASE_URL = None
BASE_DIR = ""

def get_libs_location(package: str, lib_file: str) -> str:
    import shlex
    import subprocess

    output = subprocess.run([f"{package}-config", "--libs"], capture_output=True)
    parts = shlex.split(output.stdout.decode())
    lib_path = None

    for part in parts:
        if part.startswith("-L"):
            lib_path = part[2:]

    if lib_path:
        return str(Path(lib_path) / lib_file)



def get_package_version() -> str:
    """
    Trying to get the current package version using the metadata module. This
    assumes that the version is indeed set in pyproject.toml and that the
    package was cleanly installed.
    """

    try:
        return metadata.version("arquitectos")
    except metadata.PackageNotFoundError:
        return "0.0.0"


with EnvManager(ModelWDjango()) as env:
    # ---
    # Apps
    # ---

    INSTALLED_APPS = [
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "arquitectos.apps.realtime",
        "arquitectos.apps.cms",
        "arquitectos.apps.people",
    ]

    # ---
    # Plumbing
    # ---

    ROOT_URLCONF = "arquitectos.django.urls"

    WSGI_APPLICATION = "arquitectos.django.wsgi.application"
    ASGI_APPLICATION = "arquitectos.django.asgi.application"

    # ---
    # Auth
    # ---

    AUTH_USER_MODEL = "people.User"

    # ---
    # i18n
    # ---

    LANGUAGES = [
        ("en", "English"),
    ]

    # ---
    # OpenAPI Schema
    # ---

    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

    SPECTACULAR_SETTINGS = {
        "TITLE": "arquitectos",
        "VERSION": get_package_version(),
        "SERVE_INCLUDE_SCHEMA": False,
        "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
        "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
        "REDOC_DIST": "SIDECAR",
    }

    # ---
    # Wagtail
    # ---

    WAGTAIL_SITE_NAME = "arquitectos"
    WAGTAILIMAGES_IMAGE_MODEL = "cms.CustomImage"
    WAGTAILDOCS_DOCUMENT_MODEL = "cms.CustomDocument"


    # --- Fix legacy OSes ---
    if env.get("OSX_IS_FANTASTIX", False, is_yaml=True):
        GDAL_LIBRARY_PATH = env.get(
            "GDAL_LIBRARY_PATH", get_libs_location("gdal", "libgdal.dylib")
        )
        GEOS_LIBRARY_PATH = env.get(
            "GEOS_LIBRARY_PATH", get_libs_location("geos", "libgeos_c.dylib")
        )
