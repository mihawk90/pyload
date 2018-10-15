# -*- coding: utf-8 -*-
import datetime
from builtins import _

from pyload.plugins.internal.addon import Addon
from pyload.plugins.utils import seconds_to_nexthour


class LogMarker(Addon):
    __name__ = "LogMarker"
    __type__ = "addon"
    __version__ = "0.08"
    __pyload_version__ = "0.5"
    __status__ = "testing"

    __config__ = [
        ("activated", "bool", "Activated", False),
        ("mark_hour", "bool", "Mark hours", True),
        ("mark_day", "bool", "Mark days", True),
    ]

    __description__ = """Print a mark in the log"""
    __license__ = "GPLv3"
    __authors__ = [("Walter Purcaro", "vuolter@gmail.com")]

    def activated(self):
        self.periodical.start(
            1 * 60 * 60 - 1, delay=seconds_to_nexthour(strict=True) - 1
        )

    def periodical_task(self):
        if self.config.get("mark_day") and datetime.today().hour == 0:
            self.log_info("------------------------------------------------")
            self.log_info(_("------------------- DAY MARK -------------------"))
            self.log_info("------------------------------------------------")

        elif self.config.get("mark_hour"):
            self.log_info("------------------------------------------------")
            self.log_info(_("------------------- HOUR MARK ------------------"))
            self.log_info("------------------------------------------------")
