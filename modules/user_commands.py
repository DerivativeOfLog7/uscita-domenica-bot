import telegram
import telegram.ext
import telegram.error
from modules import strings


async def cmd_pinnedpoll(silent: bool, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
	"""/pinnedpoll or /noisypoll
	NOTE: apparently bots need to be admins to pin messages, even if the permission is given to regular users in the group
	https://docs.python-telegram-bot.org/en/stable/telegram.bot.html#telegram.Bot.pin_chat_message"""
	msg = await cmd_poll(update, context)
	try:
		await msg.pin(disable_notification=silent)
	except telegram.error.Forbidden:
		pass  # Silently fail pinning if the bot doesn't have the rights to pin messages


async def cmd_poll(update: telegram.Update, context: telegram.ext.CallbackContext) -> telegram.Message:
	"""/poll
	Also called internally by the other two commands"""
	opts = [strings.OPT_1, strings.OPT_2, strings.OPT_3, strings.OPT_4]
	msg = await context.bot.send_poll(
		chat_id=update.effective_chat.id,
		question=(strings.DEFAULT_MSG if context.args in (None, []) else " ".join(context.args)),
		# Yes this discards long whitespace sequences in the message (eg "/poll foo     bar" → "foo bar") , but for what i use it for it's not an issue
		options=opts,
		is_anonymous=False,
		allows_multiple_answers=False
	)
	return msg


async def cmd_start(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
	"""/start"""
	await update.effective_chat.send_message(strings.START_MESSAGE)
