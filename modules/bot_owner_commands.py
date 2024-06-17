import sys
import typing
import telegram
import telegram.ext
import functools
import os
from modules import common, strings


def is_owners_private_chat(update: telegram.Update, context: telegram.ext.CallbackContext) -> bool:
	"""Check if a message was recived from the bot owner in private chat"""
	return update.effective_user.id == context.application.bot_data["config"].owner_user_id and update.effective_chat.type == telegram.constants.ChatType.PRIVATE


def bot_owner_only_command() -> typing.Callable:
	"""Decorator for bot owner only commands"""
	def wrapper(func):
		@functools.wraps(func)
		async def wrapped(update: telegram.Update, context: telegram.ext.CallbackContext):
			if is_owners_private_chat(update, context):
				return await func(update, context)

		return wrapped

	return wrapper


@bot_owner_only_command()
async def cmd_stop_bot(update: telegram.Update, context: telegram.ext.CallbackContext):
	"""/stop_bot"""
	await common.sysmessage_bot_stopping(context.application)
	context.application.stop_running()


@bot_owner_only_command()
async def cmd_get_log_file(update: telegram.Update, context: telegram.ext.CallbackContext):
	"""/get_log_file"""
	fname = context.application.bot_data["config"].log_file_name
	if (not os.path.isfile(fname)) or os.path.getsize(fname) == 0:
		await update.effective_chat.send_message(text=strings.EMPTY_LOG_FILE)
	else:
		with open(context.application.bot_data["config"].log_file_name, "rb") as f:
			await update.effective_chat.send_document(document=f)


@bot_owner_only_command()
async def cmd_owner_help(update: telegram.Update, context: telegram.ext.CallbackContext):
	"""/owner_help"""
	await update.effective_chat.send_message(text=strings.OWNER_HELP)
