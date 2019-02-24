from time import sleep
import telegram
from telegram.error import NetworkError, Unauthorized
import unicodedata
from threading import Thread

update_id = None
token = ""

class main():
	
	def runBot(self, bot):
		self.bot = bot
		try:
			update_id = self.bot.getUpdates()[0]['update_id']
		except IndexError:
			update_id = None
		print("last update_id {}".format(update_id))
		sleep(1)
		while True:
			try:
				for update in self.bot.getUpdates(offset=update_id, timeout=4):
					update_id = update.update_id + 1
					try:
						thBot = Thread(target=cyBot,args=[bot,update])
						thBot.start()
					except:
						pass
					sleep(0.2)
			except NetworkError:
				sleep(1)
			except Unauthorized:
				update_id += 1

class misc():

	def isAdm(user_id, admin_list):
		for adm in admin_list:
			admid = adm.user.id
			if admid == user_id:
				return True
		return False
	
	def isArabic(first_name):
		for letter in first_name:
			try:
				encoding = unicodedata.name(letter).lower()
				if 'arabic' in encoding or 'persian' in encoding:
					return True
			except ValueError:
				pass
		return False

class cyBot():
	allowed_chats = [-1001218498698, -1001171687704, -1001252516868, -1001159342300]
	mimetypes = ["application/pdf", "application/epub+zip", "application/x-mobipocket-ebook", "application/msword", "application/x-bittorrent", "text/plain", "application/x-rar-compressed", "application/zip", "application/x-7z-compressed", "audio/mpeg", "audio/mp3", "application/octet-stream"]
	misc = misc()
	log_channel = "-1001183412743"
	file_channel = "@cyfiles"
	backup_channel = "@pr1v8_board"
	replytomessage = False

	def __init__(self, bot, update):
		if update and update.message or update.callback_query:
			self.bot = bot
			self.update = update
			try:
				self.chat_id = self.update.message.chat.id
				self.message_id = self.update.message.message_id
			except:
				pass
		else:
			return

		
		
		if self.update.message:
			if self.update.message.reply_to_message:
				self.replytomessage = True
				self.target_user_id = self.update.message.reply_to_message.from_user.id
				self.target_message_id = self.update.message.reply_to_message.message_id
				self.target_fname = self.update.message.reply_to_message.from_user.first_name
				self.target_username = update.message.reply_to_message.from_user.username
		
			if update.message.document:
					file_id = self.update.message.document.file_id
					file_name = self.update.message.document.file_name
					file_size = self.update.message.document.file_size
					file_mimetype = self.update.message.document.mime_type
					# make backup of file
					if file_mimetype in self.mimetypes:
						file_data = "`{id}` -- *{name}*\n_{size}_ | {mimetype}\n\nby: #id{uid}".format(id=file_id,name=file_name,size=file_size,mimetype=file_mimetype,uid=update.message.from_user.id)

						self.bot.sendDocument(chat_id=self.file_channel, caption=file_data, parse_mode="Markdown", document=file_id, disable_notification=1)
			
			if self.update.message.new_chat_members:
					for member in self.update.message.new_chat_members:
						if misc.isArabic(member.first_name):
							self.bot.kickChatMember(chat_id=self.chat_id, user_id=member.id)
							self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="HTML", text="<b>[ban]</b>  <i>allahu akabur!1!</i>")
							return
						fname = member.first_name.replace('_', '\_')
						log_nmember = "{fname}\n`#id{id}`\n\nIn: {ctitle}\n> [{fname}](tg://user?id={id})".format(fname=fname,id=member.id,ctitle=update.message.chat.id)
						
						self.bot.restrictChatMember(chat_id=self.chat_id, user_id=member.id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)
						
						self.bot.sendMessage(chat_id=self.log_channel, parse_mode="Markdown", text=log_nmember)
						captcha = [
							[
								telegram.InlineKeyboardButton("ClickMe",callback_data=member.id)
							]
						]

						reply_markup = telegram.InlineKeyboardMarkup(captcha)
						self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text="**welcome!\n[simple user verification]**", reply_markup=reply_markup)
		
		
		if self.update.callback_query:
			tgcll = Thread(self.tgCallback())
			tgcll.start()
		
		if self.update.message and self.update.message.chat.id in self.allowed_chats:
			tgmsg = Thread(self.tgMessage())
			tgmsg.start()


	def tgMessage(self):
		if not self.update.message.text:
			return
		admin_list = self.bot.getChatAdministrators(chat_id=self.chat_id)
		user_id = self.update.message.from_user.id
		user_fname = self.update.message.from_user.first_name
		sudo = misc.isAdm(user_id, admin_list)
		txt = self.update.message.text.split(" ")
		command = txt[0]
		remain_txt = ' '.join(txt[1:])
		
		if not remain_txt:
			remain_txt = "-"
		
		if command == "/getme":
			me = self.bot.getMe()
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text="@" + me.username)
		elif command == "/sudo" and sudo:
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text="hello root")
		elif command == "/free" and self.replytomessage and sudo:
			self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text="user liberado")
		elif command == "/link":
			link = self.bot.exportChatInviteLink(chat_id=self.chat_id)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text=link)
		elif command == "/afk" or command == "/off":
			afk = "*user* [{fname}](tg://user?id={id}) *is afk*\n    *> {reason}*".format(fname=user_fname,id=user_id,reason=remain_txt)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=afk)
		elif command == "/back" or command == "/on":
			back = "*user* [{fname}](tg://user?id={id}) *is back*".format(fname=user_fname,id=user_id)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=back)
		elif command == "/ban" and self.replytomessage and sudo:
			ban = "*user* [{fname}](tg://user?id={id}) *banned*".format(fname=self.target_fname,id=self.target_user_id)
			self.bot.kickChatMember(chat_id=self.chat_id, user_id=self.target_user_id)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=ban)
		elif command == "/unban" and self.replytomessage and sudo:
			unban = "*user* [{fname}](tg://user?id={id}) *unbanned*".format(fname=self.target_fname,id=self.target_user_id)
			self.bot.unbanChatMember(chat_id=self.chat_id, user_id=self.target_user_id)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=unban)
		elif command == "/mute" and self.replytomessage and sudo:
			mute = "*user* [{fname}](tg://user?id={id}) *muted*".format(fname=self.target_fname,id=self.target_user_id)
			self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=mute)
		elif command == "/unmute" and self.replytomessage and sudo:
			unmute = "*user* [{fname}](tg://user?id={id}) *unmuted*".format(fname=self.target_fname,id=self.target_user_id)
			self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=unmute)
		elif command == "/pin" and self.replytomessage and sudo:
			self.bot.pinChatMessage(chat_id=self.chat_id, message_id=self.target_message_id,disable_notification=1)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text="*message pinned*")
		elif command == "/uinfo" and self.replytomessage and sudo:
			uinfo = "*user info* | [{fname}](tg://user?id={id})\nname: {fname}\nid: `#id{id}`\nusername: @{username}".format(fname=self.target_fname,id=self.target_user_id,username=self.target_username)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=uinfo)
		elif command == "/ginfo":
			gmember = self.bot.getChatMembersCount(chat_id=self.chat_id)
			ginfo = "*group info* | [{title}](tg://chat?id={id})\nTitle: {title}\nid: `{id}`\nMembers: {count}".format(title=self.update.message.chat.title,id=self.chat_id,count=gmember)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text=ginfo)
		elif command == "/sendfile" and sudo:
			if len(txt) != 2:
				return
			self.bot.sendDocument(chat_id=self.chat_id,reply_to_message_id=self.message_id,document=txt[1])
		elif command == "/save" and self.replytomessage and sudo:
			self.bot.forwardMessage(chat_id=self.backup_channel, from_chat_id=self.chat_id, message_id=self.target_message_id)
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
					telegram.InlineKeyboardButton("r/cyberpub", url="https://www.reddit.com/r/cyberpub/"),
					telegram.InlineKeyboardButton("Twitter", url="https://twitter.com/0xpr1v8")
				],
				[
					telegram.InlineKeyboardButton("cyGithub", url="https://github.com/cyberpunkrs/")
				]
			]   
			reply_markup = telegram.InlineKeyboardMarkup(links_list)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text="**cyNetwork**", parse_mode="Markdown", reply_markup=reply_markup)
			
		elif command == "@adm":  
			adms = ""
			for adm in admin_list:
				username = adm.user.username
				if not username:
					username = " - @null"
				else:
					username = "- @{}".format(username)
				adms += "<a href=\"tg://user?id={id}\">{fname}</a> {username}\n".format(fname=adm.user.first_name,id=adm.user.id,username=username)
			self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="HTML", text=adms)


	def tgCallback(self):
		cid = self.update.callback_query.message.chat.id
		uid = str(self.update.callback_query.from_user.id)

		if self.update.callback_query.data == uid:	
			self.bot.restrictChatMember(chat_id=cid, user_id=self.update.callback_query.from_user.id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
			
			self.bot.deleteMessage(chat_id=cid, message_id=self.update.callback_query.message.message_id)
				
			self.bot.sendMessage(chat_id=cid, reply_to_message_id=self.update.callback_query.message.reply_to_message.message_id, parse_mode="HTML", text="user <b>{}</b> liberado".format(self.update.callback_query.from_user.first_name))


if __name__ == '__main__':
	bot = main()
	btobj = telegram.Bot(token)
	bot.runBot(btobj)
