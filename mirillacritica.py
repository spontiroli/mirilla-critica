import telebot
import imdb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.cfg')

TELEGRAM_TOKEN = config.get('telegram', 'token')
SPOTIPY_ID = config.get('spotipy', 'id')
SPOTIPY_SECRET = config.get('spotipy', 'secret')

# Inicializar el bot con el token de Telegram proporcionado
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Gestor de mensajes para el comando de /ayuda.
@bot.message_handler(commands=["ayuda"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
    Hola, soy Mirilla bot, estos son los comandos disponibles:\n
    /film - buscar una película (en IMdb)
    /show - listar los últimos episodios del podcast
    /random - una película al azar de las mejores 250 de IMdb
    /frases - ¿te sientes afortunado, punk?
    /recomendada - si Mirilla lo dice... tenés que verla!
    /acerca - y entonces... ¿qué es Mirilla Crítica?
    /ayuda - despacio cerebrito
    """,
    )

# Gestor de mensajes para el comando /film
@bot.message_handler(commands=["film"])
def buscar(message):
    bot.send_message(message.chat.id, 
                     "\N{ROBOT FACE} Buscando... " + message.text[5:])
    ia = imdb.IMDb()
    items = ia.search_movie(message.text.lower()[5:])

    # DEBUG
    # bot.send_message(message.chat.id, 
    #                  str(items))
    # MOVIE CAMERA - TELEVISION - CINEMA

    parsed_results = ""

    for i in items:
        title = str(i.get('title','N/A'))
        year = str(i.get('year','N/A'))
        id = str(i.getID())
        parsed_results += f"\N{CINEMA} {title} ({year}) - [{id}](https://www.imdb.com/title/tt{id}/) \n"

    bot.send_message(
        message.chat.id, parsed_results, parse_mode = "Markdown", disable_web_page_preview = True
    )

# Gestor de mensajes para el comando /show
@bot.message_handler(commands=["show"])
def buscar(message):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    mirilla_id = "1eVHGEIbinjGluc3hajlJP"
    show = sp.show(mirilla_id)
    episodes = show['episodes']['items']

    for p in episodes:
        print(p)
        bot.send_message(message.chat.id, str(p))


@bot.message_handler(commands=["acerca"])
def buscar(message):
    bot.send_message(message.chat.id, """ MIRILLA CRITICA""")

# Gestor de mensajes para textos generales
@bot.message_handler(content_types=["text"])
def hola(message):
    if message.text.lower() in ["hola", "hello", "hi"]:
        bot.send_message(
            message.chat.id,
            f"Hola {message.from_user.first_name}, ¿en qué te puedo ayudar?",
        )
    else:
        bot.send_message(
            message.chat.id,
            "Comando no encontrado. Por favor, usa /ayuda para revisar los comandos disponibles",
        )

if __name__ == "__main__":
    # Comenzar bot
    bot.polling()