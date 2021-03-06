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
import urllib.request
import uuid



class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        print("Encountered some data  :", data)
        return data

def get_scp(url):
    req = urllib3.PoolManager()
    res = req.request('GET', url)

    soup = BeautifulSoup(res.data, 'html.parser')
    scps = soup.findAll("div",{"id":"main-content"})


    for scps in scps:
        scp_details = dict()
        scp_details['name'] = scps.find('p').text
        scp_details['content'] = scps.findAll('p')
        f = 0
        for i in scp_details['content']:
            i = i.text
            if i.count("Description: ") >= 1:
                scp_details['mainbody'] = scp_details['content'][f].text
                break
            f += 1
        f = 0
        for i in scp_details['content']:
            print(i)
            print(i.text)
            i = i.text
            if i.count("Object Class:") == 1:
                scp_details['class'] = scp_details['content'][f].text
                break
            else:
                scp_details['class'] = "UNKOWN"
            f += 1
        scp_details['image'] = scps.findAll('img')

        return scp_details


parser = MyHTMLParser()

bot = commands.Bot("?")

x = []
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))


    async def on_message(self, message):
        if message.author.id != client.user.id:
            print('Message from {0.author}: {0.content}'.format(message))
            #await message.channel.send(message.content)
            try:
                scpnum = [int(i) for i in message.content.split() if i.isdigit()] 
                if not scpnum:
                    scpnum = []
                    tempnum = message.content.split(" ")
                    for i in tempnum:
                        if i.upper().find("SCP-") > -1:
                            scpnum.append(i)
                if len(scpnum) > -1:
                    start = time.time()
                    if isinstance(scpnum[0], int) == True:
                        for num in scpnum:
                            while len(str(num)) < 3 and len(str(num)) > 0:
                                num  = str( "0" + str(num) )
                            #if num.isalpha == True:
                                #num = num[3:]
                            if len(str(num)) >= 3:
                                link = "http://www.scp-wiki.net/scp-{0}".format(num)                   
                                scp_det = get_scp(link)
                                scp_name = scp_det['name']
                                scp_class = scp_det['class'][14:]
                                scp_image = scp_det['image']
                                print(scp_image)
                                scp_content = scp_det['content']
                                scp_content1 = scp_content[3].text
                                scp_content2 = scp_content[5].text[0:(800 - len(scp_content1))]
                                scp_content3 = "{0}\n{1}...".format(scp_content1,scp_content2)
                                if len(scp_content3) <= 40:
                                    scp_content3 = scp_det['mainbody']
                                if len(scp_content3) >= 1024:
                                    scp_content3 = "{0}...".format(scp_content3[:797]) 
                                embed = discord.Embed(title="SCP-{0}".format(num),url=link,color=0xff0000)
                                print(scp_image)
                                if not scp_image:
                                    embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg")
                                else:
                                    unique_filename = str(uuid.uuid4())
                                    if scp_image[0].get('src') != "http://scp-wiki.wdfiles.com/local--files/component:heritage-rating/scp-heritage-v3.png":
                                        embed.set_thumbnail(url=scp_image[0].get('src'))
                                        urllib.request.urlretrieve(scp_image[0].get('src'), "img/{0}.png".format(unique_filename))
                                    else:
                                        if len(scp_image) > 0:
                                            embed.set_thumbnail(url="https://i.redd.it/f1u2wf28nqn21.jpg")
                                        else:
                                            embed.set_thumbnail(url=scp_image[1].get('src'))
                                embed.add_field(name="SCP CLASS:", value="{0}".format(scp_class), inline=False)
                                embed.add_field(name="CONTENT:", value="{0}".format(scp_content3), inline=False)
                                await message.channel.send(embed=embed)
                                print("Took {0:0.5f} seconds to process, {1}".format(time.time() - start, scp_name))
                    else:
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
                print("Message:{0} | Most likely not a scp request".format(message.content))
                


client = MyClient()
client.run(disbotsettings.token)

