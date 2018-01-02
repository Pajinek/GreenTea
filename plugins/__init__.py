import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

pathplugin = os.path.join(settings.ROOT_PATH, "plugins")

plugins = [f for f in os.listdir(
    pathplugin) if os.path.isdir(os.path.join(pathplugin, f))]
loaded_plugins = []

for it in plugins:
    if it in settings.ENABLE_PLUGINS:
        __import__("%s.%s" % ("plugins", it))
        loaded_plugins.append(it)

logger.info("Load plugins: %s" % ", ".join(loaded_plugins))
