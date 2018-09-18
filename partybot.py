import discord
import asyncio
import random
import logging
import youtube_dl
import pandas as pd
import bot_token


logging.basicConfig(level=logging.INFO)

if not discord.opus.is_loaded():
    discord.opus.load_opus()

client = discord.Client()

songs=pd.read_csv('songlist.csv', sep=',',header=None)
songs = songs.values

current_player = None

def after_behavior(voice):
    #fut = asyncio.run_coroutine_threadsafe(voice.disconnect(), voice.loop)
    asyncio.run_coroutine_threadsafe(voice.disconnect(), voice.loop)


async def play_url(voice, volume, url=None):
	global current_player
	'''
	if url is None: 
		#called from after - referencing https://stackoverflow.com/questions/49720659/how-can-i-play-a-list-of-songs-with-my-discord-bot-discord-py
		song_num = random.randint(0, len(songs)-1)
		print(songs[song_num][1])
		url = songs[song_num][0]
	if current_player is None:
		current_player = await voice.create_ytdl_player(url, after=lambda: after_behavior(voice))
		current_player.start()
	else:
		if not current_player.is_playing():
			current_player = await voice.create_ytdl_player(url, after=lambda: after_behavior(voice))
			current_player.start()
	'''
	
	player = await voice.create_ytdl_player(url, after = lambda: after_behavior(voice))
	player.volume = volume
	current_player = player
	player.start()

async def party(message):
	voice = await client.join_voice_channel(message.author.voice.voice_channel)
	await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
	song_num = random.randint(0, len(songs)-1)
	print(songs[song_num][1])
	await play_url(voice, songs[song_num][2], songs[song_num][0])
	# print(current_player.title)

async def newsong(message):
	print(current_player.title)
	if client.is_voice_connected(message.server):
		for voice in list(client.voice_clients):
			if (voice.server == message.server):
				player = current_player
				player.pause()
				player = None
				song_num = random.randint(0, len(songs)-1)
				print(songs[song_num][1])
				await play_url(voice, songs[song_num][2], songs[song_num][0])
	await client.delete_message(message)
				
async def endparty(message):
	if client.is_voice_connected(message.server):
		for voice in list(client.voice_clients):
			if (voice.server == message.server):
				await voice.disconnect()
	
async def bill(message):
	await client.send_message(message.channel, 'Party at Bill\'s!')
	voice = await client.join_voice_channel(client.get_channel('439547516388900874'))
	await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
	await play_url(voice, 2, 'https://www.youtube.com/watch?v=CXerF6crDRs')#pizza
	
	for channel in message.server.channels:
		if channel != client.get_channel('439547516388900874'):
			for member in list(channel.voice_members):
				print(member.name)
				if member.name != "Valid" :
					await client.move_member(member, client.get_channel('439547516388900874')) #Bill's New Internet id	
					
async def escape(message):
	voice = await client.join_voice_channel(message.author.voice.voice_channel)
	await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
	await play_url(voice, 0.2, 'https://www.youtube.com/watch?v=TQHbVGFZ0v0')

async def cumify(message):
	members = message.server.members
	candidates = []
	for member in members:
		role_ids = []
		for role in member.roles:
			role_ids.append(role.id)
		if ('236286122043506688' not in role_ids): #pussy_master role id
			candidates.append(member)

	cum_names = ['Cum', 'Cumjamin', 'Cumboy', 'Cumlad', 'Cum Together', 'Cummy', 'Cummice', 
		'Cum-a-loo', 'Mordecum', 'Cuminic', 'Cumigail', 'Elizacum', 'Cumtoria', 'Cumexander',
		'Jackcum', 'Secumstain', 'Cumtopher', 'Lincum', 'Jonacum', 'Cumeron', 'Xcumier',
		'Leonardcum', 'Harricum', 'Addicum', 'Cumanda', 'Cumroline', 'Cumsha']
	candidate = random.choice(candidates)
	cum_name = random.choice(cum_names)
	print(candidate.name, '->', cum_name)
	await client.change_nickname(candidate, cum_name)
	await client.send_message(message.channel, 'Cumification cumplete...\n{}, your new name is {}'.format(candidate.name, cum_name))
	
@client.event
async def on_message(message):
	if message.content.startswith('!bill'):
		await bill(message)

	if message.content.startswith('!party'):
		await party(message)
		
	if message.content.startswith('!escape'):
		await escape(message)
	
	if message.content.startswith('!cumify'):
		await cumify(message)
		
	if message.content.startswith('!endparty'):
		await endparty(message)
					
	if message.content.startswith('!newsong'):
		await newsong(message)
					
	#this doesn't work yet
	if (message.content.startswith('!playlist')):
		voice = await client.join_voice_channel(message.author.voice.voice_channel)
		await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
		print("playlist")
		await play_url(voice, 0.2, 'https://www.youtube.com/watch?v=tfGPv2qFOf8&list=PLr4fTgz_grSUdMgeq5nPGmwUrOwhnXGW9')

@client.event
async def on_voice_state_update(before, after):
	if (before.id == client.user.id):
		if (after.voice.mute or after.voice.deaf):
			await client.server_voice_state(after, mute = False, deafen = False)

if __name__ == "__main__":
	client.run(bot_token.token)