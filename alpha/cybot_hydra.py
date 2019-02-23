'''
simple bot for your group #beta #ignorethiscode
 imported from https://gist.github.com/pr1mx/c7ba153d9ff010bb518d0b20841fa553
 
 bot running on renegades group
'''
import os
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from requests import get
from configparser import ConfigParser
import unicodedata

update_id = None
mimetypes = ["application/pdf", "application/epub+zip", "application/x-mobipocket-ebook", "application/msword", "application/x-bittorrent", "text/plain", "application/x-rar-compressed", "application/zip", "application/x-7z-compressed", "audio/mpeg", "audio/mp3"]
token = ""

def main():
	"""Run the bot."""
	global update_id, token

	# Read from environment variable TG_BOT_TOKEN if set.
	try:
		if not token and os.environ.get('TG_BOT_TOKEN'):
			token = os.environ.get('TG_BOT_TOKEN')
		elif token and not os.environ.get('TG_BOT_TOKEN'):
			pass
		else:
			exit(1)
	except:
		print("Set token local variable TG_BOT_TOKEN or set api key at line 9 of this script")
		exit(1)
	# Telegram Bot Authorization Token
	bot = telegram.Bot(token)

	# get the first pending update_id, this is so we can skip over it in case
	# we get an "Unauthorized" exception.
	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	while True:
		try:
			cyBot(bot)
		except NetworkError:
			sleep(1)
		except Unauthorized:
			# The user has removed or blocked the bot.
			update_id += 1

def isAdm(admin_list, id):
	for adm in admin_list:
		admid = adm.user.id
		if admid == id:
			return True
	return False

def isArabic(target):
	for letter in target:
		letter = str(letter)
		encoding = unicodedata.name(letter).lower()
		if 'arabic' in encoding or 'persian' in encoding:
			return True
	return False

def cyBot(bot):
	global update_id, mimetypes

	# Request updates after the last update_id
	for update in bot.get_updates(offset=update_id, timeout=10):
		update_id = update.update_id + 1
		# debug
		allowed_chats = [-1001218498698, -1001171687704, -1001252516868, -1001159342300]

		if update and update.message and update.message.chat.id in allowed_chats:
			chat_id = update.message.chat.id
			message_id = update.message.message_id
			backup_channel = "@pr1v8_board"
			log_channel = "-1001183412743"
			replytomessage = False
			admin_list = bot.getChatAdministrators(chat_id=chat_id)

			#print("\nupdate: {}\n".format(update))


			if update.message.reply_to_message:
				replytomessage = True
				target_user_id = update.message.reply_to_message.from_user.id
				target_message_id = update.message.reply_to_message.message_id
				target_fname = update.message.reply_to_message.from_user.first_name
				target_username = update.message.reply_to_message.from_user.username


			if update.message.document:
				file_id = update.message.document.file_id
				file_name = update.message.document.file_name
				file_size = update.message.document.file_size
				file_mimetype = update.message.document.mime_type
				# make backup of file
				if file_mimetype in mimetypes:
					file_data = "`{id}` -- *{name}*\n_{size}_ | {mimetype}\n\nby: `#id{uid}`".format(id=file_id,name=file_name,size=file_size,mimetype=file_mimetype,uid=update.message.from_user.id)

					bot.sendDocument(chat_id=log_channel, caption=file_data, parse_mode="Markdown", document=file_id, disable_notification=1)

			if update.message.new_chat_members:
				for member in update.message.new_chat_members:
					if isArabic(member.first_name):
						bot.kickChatMember(chat_id=chat_id, user_id=member.id)
						bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="HTML", text="<b>[ban]</b>  <i>allahu akabur!1!</i>")
						return
						
					fname = member.first_name.replace('_', '\_')
					log_nmember = "{fname}\n`#id{id}`\n\nIn: {ctitle}\n> [{fname}](tg://user?id={id})".format(fname=fname,id=member.id,ctitle=update.message.chat.id)
					
					
					bot.restrictChatMember(chat_id=chat_id, user_id=member.id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)
					
					bot.sendMessage(chat_id=log_channel, parse_mode="Markdown", text=log_nmember)
					captcha = [
						[
							telegram.InlineKeyboardButton("i'm not a robot'",callback_data=member.id)
						]
					]

					reply_markup = telegram.InlineKeyboardMarkup(captcha)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, text="[simple user verificartion]", parse_mode="Markdown", reply_markup=reply_markup)
					#bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=welcome_message)

			if update.message.text:
				
				user_id = update.message.from_user.id
				user_fname = update.message.from_user.first_name
				txt = update.message.text.split(" ")
				command = txt[0]
				remain_txt = ' '.join(txt[1:])
				sudo = isAdm(admin_list, user_id)

				if not remain_txt:
					remain_txt = "-"

				if command == "/getme":
					me = bot.getMe()
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, text="@" + me.username)
				elif command == "/link":
					link = bot.exportChatInviteLink(chat_id=chat_id)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, text=link)
				elif command == "/afk" or command == "/off":
					afk = "*user* [{fname}](tg://user?id={id}) *is afk*\n    *> {reason}*".format(fname=user_fname,id=user_id,reason=remain_txt)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=afk)
				elif command == "/back" or command == "/on":
					back = "*user* [{fname}](tg://user?id={id}) *is back*".format(fname=user_fname,id=user_id)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=back)
				elif command == "/ban" and replytomessage and sudo:
					ban = "*user* [{fname}](tg://user?id={id}) *banned*".format(fname=target_fname,id=target_user_id)
					bot.kickChatMember(chat_id=chat_id, user_id=target_user_id)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=ban)
				elif command == "/unban" and replytomessage and sudo:
					unban = "*user* [{fname}](tg://user?id={id}) *unbanned*".format(fname=target_fname,id=target_user_id)
					bot.unbanChatMember(chat_id=chat_id, user_id=target_user_id)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=unban)
				elif command == "/mute" and replytomessage and sudo:
					mute = "*user* [{fname}](tg://user?id={id}) *muted*".format(fname=target_fname,id=target_user_id)
					bot.restrictChatMember(chat_id=chat_id, user_id=target_user_id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=mute)
				elif command == "/unmute" and replytomessage and sudo:
					unmute = "*user* [{fname}](tg://user?id={id}) *unmuted*".format(fname=target_fname,id=target_user_id)
					bot.restrictChatMember(chat_id=chat_id, user_id=target_user_id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=unmute)
				elif command == "@adm":  
					adms = ""
					for adm in admin_list:
						username = adm.user.username
						if not username:
							username = ""
						else:
							username =  username.replace('_', "\_")
							username = "- @{}".format(username)
						adms += "[{fname}](tg://user?id={id}) {username}\n".format(fname=adm.user.first_name,id=adm.user.id,username=username)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=adms)
				elif command == "/root" and sudo:
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text="*hello root*")
				elif command == "/pin" and replytomessage and sudo:
					bot.pinChatMessage(chat_id=chat_id, message_id=target_message_id,disable_notification=1)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text="*message pinned*")
				elif command == "/uinfo" and replytomessage and sudo:
					uinfo = "*user info* | [{fname}](tg://user?id={id})\nname: {fname}\nid: `#id{id}`\nusername: @{username}".format(fname=target_fname,id=target_user_id,username=target_username)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=uinfo)
				elif command == "/ginfo":
					gmember = bot.getChatMembersCount(chat_id=chat_id)
					ginfo = "*group info* | [{title}](tg://chat?id={id})\nTitle: {title}\nid: `{id}`\nMembers: {count}".format(title=update.message.chat.title,id=chat_id,count=gmember)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=ginfo)
				elif command == "/ipinfo" and sudo:
					if len(txt) != 2 or len(txt[1]) < 7:
						ip = "1.1.1.1"
					else:
						ip = txt[1]
					r = get('http://ip-api.com/json/' + ip)
					ip = r.json()
					if ip['status'] != "success":
						break
					ipinfo = "*info* | `{ip}`\n*as:* {org}\n*city:* {city}\n*country:* {code}  - {country}\n*region:* {reg}\n*isp:* {isp}\n".format(ip=ip['query'],org=ip['as'],city=ip['city'],code=ip['countryCode'],reg=ip['regionName'],country=ip['country'],isp=ip['isp'])
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text=ipinfo)
				elif command == "/sendfile" and sudo:
					if len(txt) != 2:
						break
					bot.sendDocument(chat_id=chat_id,reply_to_message_id=message_id,document=txt[1])
				elif command == "/save" and replytomessage and sudo:
					bot.forwardMessage(chat_id=backup_channel, from_chat_id=chat_id, message_id=target_message_id)
				elif command == "/db":
					if len(txt) == 1:
						listing = True
						terms = ''
					else:
						listing = False
						term = txt[1]
					
					r = ConfigParser()
					r.read('db.ini')
					
					found = False

					for v in r:
						if listing:
							terms += '{}\n'.format(v)
						
						elif v == term and not listing:
							found = True
							wiki = r[v]["INFO"]
							link = r[v]['LINK']
							break
						else:
							found = False
					
					if found:
						response = '<b>term {term}\nwiki: </b>{wiki}\n\n<b>link:</b> <a href="{link}">{link}</a>'.format(term=term,wiki=wiki,link=link)

					if listing:
						response = '<b>{}</b>'.format(terms)

					if not found and not listing:
						response = "<b>404 not found - {}</b>".format(term)


					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="HTML", text=response)
				elif command == "/cynet":
					links_list = [
						[
							telegram.InlineKeyboardButton("cyPunkrs",url="https://t.me/joinchat/DE9ViFBkvVx65PpKfvtuZg"),
							telegram.InlineKeyboardButton("R3neg4des",url="https://t.me/joinchat/K_9XAUUaKNyOpgSkf1-pbQ")
						],
						[
							telegram.InlineKeyboardButton("Parisburn", url="https://t.me/parisburns"),
							telegram.InlineKeyboardButton("warezme",url="https://t.me/warezme")
						],
						[
							telegram.InlineKeyboardButton("r/cryptobrasil", url="https://www.reddit.com/r/cryptobrasil/"),
							telegram.InlineKeyboardButton("Twitter", url="https://twitter.com/0xpr1v8")
						],
						[
							telegram.InlineKeyboardButton("cyGithub", url="https://github.com/cyberpunkrs/")
						]
					]   
					reply_markup = telegram.InlineKeyboardMarkup(links_list)
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, text="**cyNetwork**", parse_mode="Markdown", reply_markup=reply_markup)
				elif command == "/rtfm":
					bot.sendMessage(chat_id=chat_id, reply_to_message_id=message_id, parse_mode="Markdown", text="**read the fucking manual**\nhttps://en.wikipedia.org/wiki/RTFM")

		elif update and update.callback_query:
			#print("\ncallback: {}\n".format(update))
			cid = update.callback_query.message.chat.id
			uid = str(update.callback_query.from_user.id)
			
			# update.callback_query.message.from.id
			if update.callback_query.data == uid:
				
				bot.restrictChatMember(chat_id=cid, user_id=update.callback_query.from_user.id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
				bot.deleteMessage(chat_id=cid, message_id=update.callback_query.message.message_id)
				
				bot.sendMessage(chat_id=cid, reply_to_message_id=update.callback_query.message.reply_to_message.message_id, parse_mode="Markdown", text="**user {} liberado**".format(update.callback_query.from_user.first_name))
			
		else:
			sleep(2)

if __name__ == '__main__':
	main()
