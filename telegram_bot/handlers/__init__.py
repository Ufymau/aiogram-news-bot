import importlib
import os

from utils.logger_config import logger
from .news_handlers import news_all_router
from .news_handlers import news_choose_router
from .news_handlers import news_keyword_router
from .news_handlers import news_keyword_router

"""
The module dynamically loads routers from handler files (files ending in 'handler.py ')
in the current directory and collects them in the `routers` list.

- For each file with a name like `<name>_handler.py `trying to import a router named `<name>_router'.
- If the router is not found or the module is not imported, displays a warning in the log.
- At the end, it explicitly adds several routers from `news_handlers'.
- Exports the list of `routers` via `__all__'.
"""

routers = []

handlers_dir = os.path.dirname(__file__)

for handler in os.listdir(handlers_dir):
    if handler.endswith("handler.py"):

        module_name = f".{handler[:-3]}"

        basename = handler[:-3]  # example, "start_handler"
        router_name = basename[:-8] + "_router"  # delete "_handler" (8 characters) and add "_router"

        try:
            module = importlib.import_module(module_name, package=__name__)
            router = getattr(module, router_name)
            routers.append(router)
        except (ModuleNotFoundError, AttributeError) as e:
            logger.info(f"Warning: Could not load router '{router_name}' from '{module_name}': {e}")


routers.extend([
    news_choose_router,
    news_all_router,
    news_keyword_router,
])

__all__ = ["routers"]

