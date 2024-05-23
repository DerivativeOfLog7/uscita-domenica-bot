import sys
import configparser
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class ConfigDataClass:
	log_file_name: str
	bot_token: str
	owner_user_id: int
	system_messages_channel_id: int
	debugging: bool


def die(msg: str, code: int) -> None:
	print(msg, file=sys.stderr)
	sys.exit(code)


def read_config(filename: str) -> Union[ConfigDataClass, None]:
	config = configparser.ConfigParser()
	if not config.read(filename):
		raise FileNotFoundError
	return ConfigDataClass(bot_token=config.get("secrets", "bot_token"),
							owner_user_id=config.getint("secrets", "owner_user_id"),
							system_messages_channel_id=config.getint("secrets", "system_messages_channel_id"),
							log_file_name=config.get("main", "log_file_name"),
							debugging=config.getboolean("main", "debugging"))


