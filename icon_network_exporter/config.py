from enum import Enum
from typing import Any

import yaml
from pydantic import BaseSettings

RPC_URL_MAP = {
    "mainnet": {
        "main_api_endpoint": "https://ctz.solidwallet.io/api/v3",
        "end_ranking": "0x64",
    },
    "testnet": {
        "main_api_endpoint": "https://test-ctz.solidwallet.io/api/v3",
        "end_ranking": "0x7",
    },
    "zicon": {
        "main_api_endpoint": "https://zicon.net.solidwallet.io/api/v3",
        "end_ranking": "0x22",
    },
    "bicon": {
        "main_api_endpoint": "https://bicon.net.solidwallet.io/api/v3",
        "end_ranking": "0x7",
    },
}


class NetworksEnum(str, Enum):
    mainnet = "mainnet"
    zicon = "zicon"
    bicon = "bicon"
    testnet = "testnet"


class Config(BaseSettings):

    network_name: NetworksEnum = NetworksEnum.mainnet
    exporter_port: int = 6100
    exporter_address: str = ""

    main_api_endpoint: str = None
    end_ranking: str = None  # number_preps_scrape_hex

    reference_nodes: list = None
    main_watch_list_file: str = None
    main_watch_list: list = []
    sub_watch_list_file: str = None
    sub_watch_list: list = []

    num_data_points_retentation: int = 5
    poll_interval: float = 5
    poll_timeout: float = 0.5
    refresh_prep_list_count: int = 60
    parallelism: int = 1

    def __init__(self, **values: Any):
        super().__init__(**values)
        if not self.main_api_endpoint:
            self.main_api_endpoint = RPC_URL_MAP[self.network_name]["main_api_endpoint"]

        if not self.end_ranking:
            self.end_ranking = RPC_URL_MAP[self.network_name]["end_ranking"]

        if self.main_watch_list_file:
            with open(self.main_watch_list_file) as f:
                self.main_watch_list = yaml.load(f)

        if self.sub_watch_list_file:
            with open(self.sub_watch_list_file) as f:
                self.sub_watch_list = yaml.load(f)


if __name__ == "__main__":
    c = Config()
    print(c.network_name)
