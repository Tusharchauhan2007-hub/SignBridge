"""
Pages package for SignBridge Frontend.
"""

from frontend.pages.home import render_home_page
from frontend.pages.how_it_works import render_how_it_works_page
from frontend.pages.features import render_features_page
from frontend.pages.live_app import render_live_app_page
from frontend.pages.studio import render_studio_page
from frontend.pages.about import render_about_page

__all__ = [
    "render_home_page",
    "render_how_it_works_page",
    "render_features_page",
    "render_live_app_page",
    "render_studio_page",
    "render_about_page",
]

