import logging
import configparser
import telegram.error
from modules import base, common, strings, user_commands, bot_owner_commands
from modules.exceptions import *
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from functools import partial


def _main():
	try:
		config = base.read_config("bot_config.ini")
	except FileNotFoundError:
		base.die(strings.CANNOT_OPEN_CONFIG_FILE, 10)
	except (configparser.NoSectionError, configparser.NoOptionError):
		base.die(strings.MALFORMED_CONFIG_FILE, 11)
	except ValueError:
		base.die(strings.INVALID_CONFIG_VALUES, 12)

	if config.debugging:
		logging.basicConfig(
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			level=logging.DEBUG
		)
	else:
		logging.basicConfig(
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			level=logging.WARNING,
			filename=config.log_file_name
		)

	# Build application
	application = ApplicationBuilder().token(config.bot_token).build()

	# Add config
	application.bot_data["config"] = config

	# Add handlers
	handlers = [CommandHandler("start", user_commands.cmd_start),
				CommandHandler("poll", user_commands.cmd_poll),
				CommandHandler("noisypoll", partial(user_commands.cmd_pinnedpoll, False)),
				CommandHandler("loudpoll", partial(user_commands.cmd_pinnedpoll, False)),
				CommandHandler("pinnedpoll", partial(user_commands.cmd_pinnedpoll, True))]
	owner_handlers = [CommandHandler("get_log_file", bot_owner_commands.cmd_get_log_file),
					CommandHandler("glf", bot_owner_commands.cmd_get_log_file),
					CommandHandler("stop_bot", bot_owner_commands.cmd_stop_bot),
					CommandHandler("sb", bot_owner_commands.cmd_stop_bot),
					CommandHandler("owner_help", bot_owner_commands.cmd_owner_help),
					CommandHandler("oh", bot_owner_commands.cmd_owner_help)]
	application.add_handlers(handlers)
	application.add_handlers(owner_handlers)
	application.add_error_handler(callback=common.error_callback)

	# Start bot
	application.post_init = common.sysmessage_bot_started
	application.post_stop = common.sysmessage_bot_stopped

	try:
		application.run_polling()
	except telegram.error.InvalidToken:
		base.die(strings.INVALID_BOT_TOKEN, 13)
	except SystemMessagesChannelException:
		base.die(strings.SYSTEM_MESSAGES_CHANNEL_ERROR, 20)


if __name__ == "__main__":
	_main()
