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
    fut = asyncio.run_coroutine_threadsafe(voice.disconnect(), voice.loop)


async def play_url(url, voice, volume):
	global current_player
	player = await voice.create_ytdl_player(url, after = lambda: after_behavior(voice))
	player.volume = volume
	current_player = player
	player.start()

@client.event
async def on_message(message):
	if message.content.startswith('!bill'):
		await client.send_message(message.channel, 'Party at Bill\'s!')
		voice = await client.join_voice_channel(client.get_channel('439547516388900874'))
		await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
		# current_player = await play_url('https://www.youtube.com/watch?v=CXerF6crDRs', voice, 2)#pizza
		await play_url('https://www.youtube.com/watch?v=CXerF6crDRs', voice, 2)#pizza
		
		for channel in message.server.channels:
			if channel != client.get_channel('439547516388900874'):
				for member in list(channel.voice_members):
					print(member.name)
					if member.name != "Valid" :
						await client.move_member(member, client.get_channel('439547516388900874')) #Bill's New Internet id

	if message.content.startswith('!party'):
		voice = await client.join_voice_channel(message.author.voice.voice_channel)
		await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
		song_num = random.randint(0, len(songs)-1)
		print(songs[song_num][1])
		# current_player = await play_url(songs[song_num][0], voice, 0.2)
		await play_url(songs[song_num][0], voice, songs[song_num][2])
		# print(current_player.title)
		
		
	if message.content.startswith('!escape'):
		voice = await client.join_voice_channel(message.author.voice.voice_channel)
		await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
		# current_player = await play_url('https://www.youtube.com/watch?v=TQHbVGFZ0v0', voice, 0.2)
		await play_url('https://www.youtube.com/watch?v=TQHbVGFZ0v0', voice, 0.2)
	
	if message.content.startswith('!cumify'):
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
		
	if message.content.startswith('!endparty'):
		if client.is_voice_connected(message.server):
			for voice in list(client.voice_clients):
				if (voice.server == message.server):
					await voice.disconnect()
					
	if message.content.startswith('!newsong'):
		print(current_player.title)
		if client.is_voice_connected(message.server):
			for voice in list(client.voice_clients):
				if (voice.server == message.server):
					player = current_player
					player.pause()
					player = None
					song_num = random.randint(0, len(songs)-1)
					print(songs[song_num][1])
					# current_player = await play_url(songs[song_num][0], voice, 0.2)
					await play_url(songs[song_num][0], voice, songs[song_num][2])
					
	if (message.content.startswith('!playlist')):
		voice = await client.join_voice_channel(message.author.voice.voice_channel)
		await client.server_voice_state(message.server.get_member(voice.user.id), mute = False, deafen = False)
		print("playlist")
		await play_url('https://www.youtube.com/watch?v=tfGPv2qFOf8&list=PLr4fTgz_grSUdMgeq5nPGmwUrOwhnXGW9', voice, 0.2)

@client.event
async def on_voice_state_update(before, after):
	if (before.id == client.user.id):
		if (after.voice.mute or after.voice.deaf):
			await client.server_voice_state(after, mute = False, deafen = False)

if __name__ == "__main__":
	client.run(bot_token.token)