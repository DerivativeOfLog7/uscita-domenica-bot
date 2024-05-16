import telegram
import telegram.ext
import telegram.error
import typing
from modules import strings, base
from modules.exceptions import *


async def send_system_message(msg: str, app: telegram.ext.Application):
	"""Send a message to the system messages channel"""
	await app.bot.send_message(
		chat_id=app.bot_data["config"].system_messages_channel_id,
		text=f"{app.bot.name}\n"
			f"{msg}"
	)


async def sysmessage_bot_started(app: telegram.ext.Application) -> None:
	try:
		bot_user = await app.bot.get_chat_member(chat_id=app.bot_data["config"].system_messages_channel_id, user_id=app.bot.id)
		if not bot_user.can_post_messages:
			raise SystemMessagesChannelException
		await send_system_message(strings.BOT_STARTED_MESSAGE, app)
	except (telegram.error.BadRequest, telegram.error.Forbidden):
		raise SystemMessagesChannelException


async def sysmessage_bot_stopping(app: telegram.ext.Application) -> None:
	await send_system_message(strings.BOT_STOPPING_MESSAGE, app)


async def sysmessage_bot_stopped(app: telegram.ext.Application) -> None:
	try:
		await send_system_message(strings.BOT_STOPPED_MESSAGE, app)
	# Better way to do this? All this is needed because the bot would still try to send the stopped messages if the token is invalid
	except (telegram.error.BadRequest, telegram.error.Forbidden, telegram.error.InvalidToken, RuntimeError):
		pass


async def error_callback(update: typing.Optional[object], context: telegram.ext.CallbackContext):
	await send_system_message(f"{strings.BOT_ERROR_MESSAGE}\n"
								f"{context.error}", context.application)
