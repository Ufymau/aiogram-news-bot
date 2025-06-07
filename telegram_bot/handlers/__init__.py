import os
import importlib
from .news_handlers import news_choose_router
from .news_handlers import news_all_router
from .news_handlers import news_keyword_router
from utils.logger_config import logger

routers = []

handlers_dir = os.path.dirname(__file__)

for handler in os.listdir(handlers_dir):
    if handler.endswith("handler.py"):
        module_name = f".{handler[:-3]}"


        basename = handler[:-3]  # например, "start_handler"
        router_name = basename[:-8] + "_router"  # удаляем "_handler" (8 символов) и добавляем "_router"

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

