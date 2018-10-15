# -*- coding: utf-8 -*-

from pyload.network.request_factory import getURL as get_url
from pyload.plugins.internal.simplecrypter import SimpleCrypter
import json


class TenluaVnFolder(SimpleCrypter):
    __name__ = "TenluaVnFolder"
    __type__ = "crypter"
    __version__ = "0.02"
    __pyload_version__ = "0.5"
    __status__ = "testing"

    __pattern__ = r"https?://(?:www\.)?tenlua\.vn/folder/.+?/(?P<ID>[0-9a-f]+)/"
    __config__ = [
        ("activated", "bool", "Activated", True),
        ("use_premium", "bool", "Use premium account if available", True),
        (
            "folder_per_package",
            "Default;Yes;No",
            "Create folder for each package",
            "Default",
        ),
        ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10),
    ]

    __description__ = """Tenlua.vn decrypter plugin"""
    __license__ = "GPLv3"
    __authors__ = [("GammaC0de", "nitzo2001[AT]yahoo[DOT]com")]

    API_URL = "https://api2.tenlua.vn/"

    @classmethod
    def api_response(cls, method, **kwargs):
        kwargs["a"] = method
        return json.loads(get_url(cls.API_URL, post=json.dumps([kwargs])))

    def decrypt(self, pyfile):
        folder_info = self.api_response(
            "filemanager_gettree", p=self.info["pattern"]["ID"], download=1
        )
        pack_links = [
            "https://www.tenlua.vn/download/{}/{}".format(x["h"], x["ns"])
            for x in folder_info[0]["f"]
            if "h" in x and "ns" in x
        ]

        pack_name = folder_info[0]["f"][0].get("n") or self.pyfile.package().name

        if pack_links:
            self.packages.append((pack_name, pack_links, pack_name))
