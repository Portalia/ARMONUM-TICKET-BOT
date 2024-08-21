import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import os
from jproperties import Properties



configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)


if configs.get("SERVER").data == "STB":
    print("stb")
    DISCORD_TOKEN = configs.get("DISCORD_TOKEN").data
    GUILD_ID = 1109898905765810256
    TICKETS_CHANNEL_ID = 1275451976028524679
    LOG_CHANNEL_ID = 1275460076261474451
    ADMIN_ROLE_ID = 1263778828291936264
    TICKETS_CATEGORY_ID = 1109898906604675193
    activities = configs.get("ACTIVITY").data
elif configs.get("SERVER").data == "ARMONUM":
    DISCORD_TOKEN = configs.get("DISCORD_TOKEN").data
    GUILD_ID = 1263778828291936257
    TICKETS_CHANNEL_ID = 1275100516824776820
    LOG_CHANNEL_ID = 1275716127774998568
    ADMIN_ROLE_ID = 1263778828291936264
    TICKETS_CATEGORY_ID = 1275100436218773514
    activities = configs.get("ACTIVITY").data

CUSTOM_EMOJI_IDS = {
    'open': 1013527364455649430,
    'closed': 1275106019910877208,
    'opentime': 1275106052974579785,
    'claim': 1275106001959518323,
    'reason': 1275106073409359882,
    'envelop': 1275106090304143462
}



intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='-', intents=intents)
score = 0






# View class for ticket creation buttons
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(style=discord.ButtonStyle.primary, label='Général', custom_id='open_form', emoji=discord.PartialEmoji(id=CUSTOM_EMOJI_IDS['envelop'], name='envelop')))
        self.add_item(Button(style=discord.ButtonStyle.success, label='Site', custom_id='site_form', emoji=discord.PartialEmoji(id=CUSTOM_EMOJI_IDS['envelop'], name='envelop')))
        self.add_item(Button(style=discord.ButtonStyle.danger, label='Sanctions', custom_id='sanctions_form', emoji=discord.PartialEmoji(id=CUSTOM_EMOJI_IDS['envelop'], name='envelop')))

# Modal for ticket creation
class GeneralTicketModal(Modal):
    def __init__(self):
        global score, ticket_category
        super().__init__(title='Formulaire de Ticket')
        self.add_item(discord.ui.TextInput(label='VOTRE PSEUDO :', custom_id='usernameInput', style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label='VERSION :', custom_id='versionInput', style=discord.TextStyle.short, placeholder='Veuillez mettre votre version'))
        self.add_item(discord.ui.TextInput(label='PROBLÈME :', custom_id='problemInput', style=discord.TextStyle.paragraph, placeholder='Expliquez le plus clairement possible votre problème'))
        score = 1
        ticket_category = "general"

class SiteTicketModal(Modal):
    def __init__(self):
        global score, ticket_category
        super().__init__(title='Formulaire de Ticket')
        self.add_item(discord.ui.TextInput(label='VOTRE PSEUDO :', custom_id='usernameInput', style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label='DATE DU DERNIER SOUCI :', custom_id='dateInput', style=discord.TextStyle.short, placeholder='Veuillez mettre la date du dernier souci.'))
        self.add_item(discord.ui.TextInput(label='SOUCI RENCONTRE :', custom_id='problemInput', style=discord.TextStyle.paragraph, placeholder='Expliquez le plus clairement possible votre problème'))
        score = 1
        ticket_category = "site"

class SanctionTicketModal(Modal):
    def __init__(self):
        global score, ticket_category
        super().__init__(title='Formulaire de Ticket')
        self.add_item(discord.ui.TextInput(label='VOTRE PSEUDO :', custom_id='usernameInput', style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label='SANCTIONNE PAR :', custom_id='dateInput', style=discord.TextStyle.short, placeholder='Veuillez mettre le nom de l\'administrateur qui vous a sanctionné.'))
        self.add_item(discord.ui.TextInput(label='RAISON DE LA SANCTION :', custom_id='problemInput', style=discord.TextStyle.short, placeholder='Expliquez le plus clairement possible votre raison de sanction.'))
        self.add_item(discord.ui.TextInput(label='DEFENSE :', custom_id='defInput', style=discord.TextStyle.paragraph, placeholder='Expliquez le plus clairement possible votre défense.'))
        score = 1
        ticket_category = "sanction"

# Modal for closing ticket with reason
class CloseReasonModal(Modal):
    def __init__(self):
        global score
        super().__init__(title='Motif de la clôture')
        self.add_item(discord.ui.TextInput(label='Raison de la clôture', custom_id='reasonInput', style=discord.TextStyle.paragraph, placeholder='Expliquez la raison de la clôture'))
        score = 2

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    activity = discord.Game(name=activities)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    channel = bot.get_channel(1275100516824776820)
    if channel:
        print("Connecté au salon.")
        file = open('id.txt','r')
        lire = file.read()
        msg = await channel.fetch_message(lire)
        await msg.delete()
        view = TicketView()
        embed = discord.Embed(
            title='Créer un ticket',
            description='TEMPS DE PRISE EN CHARGE 24H/48H \nMerci de ne pas mentionner le staff et \nde respecter les différentes catégories.\n• En cas de non-respect = ticket fermé',
            color=0xE3DA2A
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/1274845806410596447/1275082220079546441/OIG4_1.jpg?ex=66c4985b&is=66c346db&hm=0af9eaba05bdffc0f3eb18f0b81cdecd5e7de35298188af207309c36d6c48e8c&')
        embed.set_footer(text='Créé par PORTALIA STUDIO©', icon_url='https://cdn.discordapp.com/attachments/1274845806410596447/1275082220079546441/OIG4_1.jpg?ex=66c4985b&is=66c346db&hm=0af9eaba05bdffc0f3eb18f0b81cdecd5e7de35298188af207309c36d6c48e8c&')
        msg2 = await channel.send(embed=embed, view=view)
        file.close()
        file = open('id.txt','w')
        file.write(str(msg2.id))
        print('Message de création de ticket rechargé avec succès')
    else:
        print('Salon de tickets non trouvé')

@bot.event
async def on_interaction(interaction, channel = discord.TextChannel):
    global score
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get("custom_id") == 'open_form':
            modal = GeneralTicketModal()
            await interaction.response.send_modal(modal)
        elif interaction.data.get("custom_id") == 'site_form':
            modal = SiteTicketModal()
            await interaction.response.send_modal(modal)
        elif interaction.data.get("custom_id") == 'sanctions_form':
            modal = SanctionTicketModal()
            await interaction.response.send_modal(modal)
        elif interaction.data.get("custom_id") == 'close_ticket':
            await interaction.channel.set_permissions(interaction.user, view_channel=False)
            await interaction.response.send_message('Le ticket a été fermé.', ephemeral=True)
        elif interaction.data.get("custom_id") == 'close_with_reason':
            modal = CloseReasonModal()
            await interaction.response.send_modal(modal)
        elif interaction.data.get("custom_id") == 'claim_ticket':
            guild = bot.get_guild(GUILD_ID)
            member = guild.get_member(interaction.user.id)
            if member and ADMIN_ROLE_ID in [role.id for role in member.roles]:
                await interaction.response.send_message(f'<@{ADMIN_ROLE_ID}> a réclamé ce ticket.', ephemeral=False)
            else:
                await interaction.response.send_message('Vous n\'avez pas la permission de réclamer ce ticket.', ephemeral=True)
    
    elif interaction.type == discord.InteractionType.modal_submit:
        if score == 1:
            score = 0
            global ticket_category,username
            if ticket_category == 'general':
                username = interaction.data['components'][0]['components'][0]['value']
                version = interaction.data['components'][1]['components'][0]['value']
                problem = interaction.data['components'][2]['components'][0]['value']
                channel_topic = f'Ticket ouvert par {username}\nVersion: {version}\nProblème: {problem}'
            elif ticket_category == 'site':
                username = interaction.data['components'][0]['components'][0]['value']
                date = interaction.data['components'][1]['components'][0]['value']
                pb = interaction.data['components'][2]['components'][0]['value']
                channel_topic = f'Ticket ouvert par {username}\Souci rencontré: {pb}\nDate du dernier souci: {date}'
            elif ticket_category == 'sanction':
                username = interaction.data['components'][0]['components'][0]['value']
                admin = interaction.data['components'][1]['components'][0]['value']
                sanct = interaction.data['components'][2]['components'][0]['value']
                defense = interaction.data['components'][3]['components'][0]['value']
                channel_topic = f'Ticket ouvert par {username}\Sanctionné par: {admin}\nRaison de la sanction: {sanct}\nVotre défense: {defense}'
            else:
                channel_topic = 'Category non trouvée'
            guild = bot.get_guild(GUILD_ID)
            if guild:
                category = discord.utils.get(guild.categories, id=TICKETS_CATEGORY_ID)
                channel_name = f'{username}-ticket-{ticket_category}'
                channel = await guild.create_text_channel(name=channel_name, category=category, topic=channel_topic)
                
                embed = discord.Embed(title='Ticket créé', description=ticket_category, color=0xE3DA2A)
                
                close_ticket_button = Button(style=discord.ButtonStyle.danger, label='🔒Fermer', custom_id='close_ticket')
                close_with_reason_button = Button(style=discord.ButtonStyle.danger, label='🔐 Fermer avec motif', custom_id='close_with_reason')
                claim_ticket_button = Button(style=discord.ButtonStyle.success, label='👨🏻‍💻Réclamer', custom_id='claim_ticket')
                
                view = View()
                view.add_item(close_ticket_button)
                view.add_item(close_with_reason_button)
                view.add_item(claim_ticket_button)
                
                await channel.send(embed=embed, view=view)
                
                log_channel = bot.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    if ticket_category == 'general':
                        await log_channel.send(f'Nouveau ticket créé: {channel_name}\nDe categorie: {ticket_category}\nPar: {username}\nProblème: {problem or "N/A"}\nVersion: {version}')
                    elif ticket_category == 'site':
                        await log_channel.send(f'Nouveau ticket créé: {channel_name}\nDe categorie: {ticket_category}\nPar: {username}\nDate du dernier problème: {date}\nProblème: {pb or "N/A"}')
                    elif ticket_category == 'sanction':
                        await log_channel.send(f'Nouveau ticket créé: {channel_name}\nDe categorie: {ticket_category}\nPar: {username}\nSanctionné par: {admin}\nRaison de la sanction: {sanct}\nLa défense: {defense}')
                
                await interaction.response.send_message('Votre ticket a été créé !', ephemeral=True)
            else:
                await interaction.response.send_message('Serveur non trouvé.', ephemeral=True)

        elif score == 2:
            score = 0
            reason = interaction.data['components'][0]['components'][0]['value']
            await interaction.channel.send(f'Ticket fermé pour la raison suivante : {reason}')
            await interaction.channel.set_permissions(interaction.user, view_channel=False)
            
bot.run(DISCORD_TOKEN)
