import tempget
import discord
import time
import discord
from discord.ext.commands import Bot
from discord.ext import commands 
import asyncio
import time
import datetime
import urllib3
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import disbotsettings

class MyHTMLParser(HTMLParser): # I think this creates the HTMLParser
	def handle_data(self, data):
		print("Encountered some data  :", data)
		return data

def get_scp(url): # Gets the SCP information
	req = urllib3.PoolManager()
	res = req.request('GET', url) # Sets to retrieve

	soup = BeautifulSoup(res.data, 'html.parser')
	scps = soup.findAll("div",{"id":"main-content"})


	for scps in scps: # Go through all divs | Probably very inefficient 
		scp_details = dict() 
		scp_details['name'] = scps.find('p').text # Finds the first text area | Likely to break, should fix
		scp_details['content'] = scps.findAll('p') # Gets all text areas
		f = 0
		for i in scp_details['content']: # Loop through all text areas
			i = i.text # Convert to text only
			if i.count("Description: ") >= 1: # Does it have description?
				scp_details['mainbody'] = scp_details['content'][f].text # Make mainbody equal to the description
				break # Stop loop
			f += 1
		f = 0
		for i in scp_details['content']: # Loop through all content
			print(i)
			print(i.text) # Debugging
			i = i.text
			if i.count("Object Class:") == 1: # Does it have an object class?
				scp_details['class'] = scp_details['content'][f].text # Get first piece of text after object class
				break # Stop loop
			else: # If object class not found
				scp_details['class'] = "UNKNOWN" # Make class unknown 
			f += 1
		scp_details['image'] = scps.findAll('img') # Finds all images in the page

		return scp_details # Returns everything


parser = MyHTMLParser()

bot = commands.Bot("?") # Sets the syntax for bot commands

x = []
class MyClient(discord.Client):

	scpsprocessed = 0 # Unused currently
	
	async def on_message(self, message):
		numcheck = 1 # Value of 0 allows bot to respond to all numbers in chat
		if message.author.id != client.user.id: # Dont respond to self | Removing this breaks the bot and the discord channel
			print('Message from {0.author}: {0.content}'.format(message)) # Debug for seeing recieved messages
			#await message.channel.send(message.content)
			try: # Makes bot not commit seppuku when an error occurs
				scpnum = [int(i) for i in message.content.split() if i.isdigit()]  # I think this checks if it is all numbers?
				if not scpnum: # If it is not all numbers
					scpnum = []
					tempnum = message.content.split(" ") # Split by spaces
					for i in tempnum:
						if i.upper().find("SCP-") > -1: # If it has scp then store it intp scpnum
							scpnum.append(i)
				if len(scpnum) > -1: # If scpnum has something stored
					start = time.time() # Debugging to check time 
					if isinstance(scpnum[0], int) == True and numcheck == 0: # Is it all numbers?
						for num in scpnum: # For all numbers in scpnum
							while len(str(num)) < 3 and len(str(num)) > 0: # If the number is less than 100 and does not 3 digits in length
								num  = str( "0" + str(num) ) # Prepends a 0 onto the number
							#if num.isalpha == True:
								#num = num[3:]
							if len(str(num)) >= 3: # Only execute if the number has more than 2 digits
								link = "http://www.scp-wiki.net/scp-{0}".format(num) # Formats the link correctly           
								scp_det = get_scp(link) # Get all details from the link
								scp_name = scp_det['name'] # Get scp name
								scp_class = scp_det['class'][14:] # Get scp class
								scp_image = scp_det['image'] # Get all images
								print(scp_image) # Idk what this is meant to do
								scp_content = scp_det['content'] # Get the content
								scp_content1 = scp_content[3].text # Seperates content for truncation
								scp_content2 = scp_content[5].text[0:(800 - len(scp_content1))] # Truncates
								scp_content3 = "{0}\n{1}...".format(scp_content1,scp_content2) # Formatting
								if len(scp_content3) <= 40: # If the content is less than 40 char then use mainbody
									scp_content3 = scp_det['mainbody']
								if len(scp_content3) >= 1024: # If over 1024 (character limit) then truncate
									scp_content3 = "{0}...".format(scp_content3[:797]) 
								embed = discord.Embed(title="SCP-{0}".format(num),url=link,color=0xff0000) # Formatting of message
								print(scp_image) # Idk what this is meant to do
								if not scp_image: # If there isnt an image
									embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg") # Use this default
								else: # If there is an image
									if scp_image[0].get('src') != "http://scp-wiki.wdfiles.com/local--files/component:heritage-rating/scp-heritage-v3.png": # Ensure the image isnt a reward thing
										embed.set_thumbnail(url=scp_image[0].get('src')) # Set thumbnail to image
									else: # If it is reward
										if len(scp_image) > 0: # Im pretty sure its meant to be less than 1 
											embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg") # Set to default
										else:
											embed.set_thumbnail(url=scp_image[1].get('src')) # Set to actual image
								embed.add_field(name="SCP CLASS:", value="{0}".format(scp_class), inline=False) # Format class
								embed.add_field(name="CONTENT:", value="{0}".format(scp_content3), inline=False) # Format content
								await message.channel.send(embed=embed) # Send the message
								print("Took {0:0.5f} seconds to process, {1}".format(time.time() - start, scp_name)) # Display time taken
					else: # Same as the previous just different link formatting
						link = "http://www.scp-wiki.net/{0}".format(scpnum)                   
						scp_det = get_scp(link)
						scp_name = scp_det['name']
						scp_class = scp_det['class'][14:]
						scp_image = scp_det['image']
						print(scp_image)
						scp_content = scp_det['content']
						scp_content1 = scp_content[3].text
						scp_content2 = scp_content[5].text[:1000 - len(scp_content1)] + "..."
						scp_content3 = "{0}\n{1}...".format(scp_content1,scp_content2)
						if len(scp_content3) <= 40:
							scp_content3 = scp_det['mainbody']
						if len(scp_content3) >= 1024:
							scp_content3 = scp_content3[:800]
						embed = discord.Embed(title="{0}".format(str(scpnum[0]).upper()),url=link,color=0xff0000)
						print(scp_image)
						if not scp_image:
							embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg")
						else:
							if scp_image[0].get('src') != "http://scp-wiki.wdfiles.com/local--files/component:heritage-rating/scp-heritage-v3.png":
								embed.set_thumbnail(url=scp_image[0].get('src'))
							else:
								if len(scp_image) > 0:
									embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg")
								else:
									embed.set_thumbnail(url=scp_image[1].get('src'))
						embed.add_field(name="SCP CLASS:", value="{0}".format(scp_class), inline=False)
						embed.add_field(name="CONTENT:", value="{0}".format(scp_content3), inline=False)
						await message.channel.send(embed=embed)
						print("Took {0:0.5f} seconds to process, {1}".format(time.time() - start, scp_name))
			except IndexError:
				print("Message:{0} | Most likely not a scp request".format(message.content)) # Makes sure the bot doesnt seppuku

	async def on_ready(self): # On ready
		import random # Imports random for the status
		print('Logged on as {0}!'.format(self.user)) # Says what it is logged in as
		scpnumber = "079" # Default value
		while True: # Executes while bot runs
			scpnumber = str(random.randint(0,5940)) # Random number generate to the highest I viewed on newest
			while len(str(scpnumber)) < 3 and len(str(scpnumber)) > 0: # Ensures the number is formatted to scp standards
				scpnumber  = str( "0" + str(scpnumber) ) # Prepends 0
			activity = discord.Game(name="Reading SCP-{0}".format(scpnumber)) # Sets the activity
			await client.change_presence(status=discord.Status.online, activity=activity) # Displays the activity
			avgtemp = 0.0 # Default temp
			minuttemp = [] # Stores all temps 
			temp = tempget.get_cpu_temperature() # Gets the cpu temp of raspberry pi
			minuttemp.append(str(temp)) # Appends the temp to minutttemp
			await asyncio.sleep(599) # Sleeps for 10 minutes
			for i in minuttemp: # Add all temps to avgtemp
				avgtemp += float(i)
			avgtemp = avgtemp / len(minuttemp) # Calculates average
			print(avgtemp) # Prints temp
			ownerAcc = client.get_user(disbotsettings.owner) # Get the bot owner
			avgtemp = "Average Temp: {0}°C\nProcessed: {1} scps".format(avgtemp,"UNKOWN") # Formatting message | This is where the processed scp value would be used
			print("Sent '{0}' to user: {1}".format(avgtemp,ownerAcc.name)) # Prints the message sent and who to
			await ownerAcc.send(avgtemp) # Send message


client = MyClient() 
client.run(disbotsettings.token) # Start bot

