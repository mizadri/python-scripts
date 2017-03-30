import telebot
import urllib2
import speech_recognition as sr
import pydub 

TOKEN = '280943985:AAHyRUXCczEZWcXu_ydlpIUkHZIuL86Px5s' 

bot = telebot.TeleBot(TOKEN)

language = {}
language["Spanish"] = "es-ES"
language["English"] = "en-GB"
language["French"] = "fr-FR"
default = "Spanish"

@bot.message_handler(commands=['config'])
def send_welcome(message):
    #mostrarTecladoIdiomas(message)
    print message.from_user

def mostrarTecladoIdiomas(message):
    #bot.reply_to(message, "Selecciona el idioma de tu audio")
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Spanish')
    markup.row("English")
    markup.row("French")
    markup.one_time_keyboard = True
    message = bot.send_message(message.chat.id, "Selecciona una accion:", reply_markup=markup)
    bot.register_next_step_handler(message, procesarOpcion)

 
def convertirAudio(chat_id,username):
    convertirOgaWav()
    convertirAudioTexto(chat_id, language[default], username)

def procesarOpcion(message): 
    default = message.text
        

def descargarArchivo(file_id): 
    file_info = bot.get_file(file_id)
    separador = file_info.file_path.split(".")
    extension = separador[len(separador)-1]
    archivoDescargar = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
    archivoGuardar = "audio."+extension
    print archivoGuardar
    print file_info.file_path
    
    descarga = urllib2.urlopen(archivoDescargar)
    ficheroGuardar=file(archivoGuardar,"w")
    ficheroGuardar.write(descarga.read())
    ficheroGuardar.close()


def convertirOgaWav(): 
    ogg_version = pydub.AudioSegment.from_ogg("audio.oga")
    ogg_version.export("audio.wav", format="wav")        


def convertirAudioTexto(chat_id, idioma, username):
    r = sr.Recognizer()
    with sr.WavFile("audio.wav") as source:             
        audio = r.record(source)
    
    try:
        KEY_BING = "0e542302909f4a29b70715e9acc99e41"
        texto = r.recognize_bing(audio,KEY_BING,idioma,False)
        bot.send_message(chat_id,"@"+username+": "+texto) 
    except LookupError:
        bot.send_message(chat_id,"No se ha podido convertir el audio")


def listener(mensajes): 
    for m in mensajes: 
        if m.content_type == 'voice':
            file_id = m.voice.file_id
            descargarArchivo(file_id)
            convertirAudio(m.chat.id,m.from_user.first_name)
            #mostrarTecladoIdiomas(m)

bot.set_update_listener(listener) 
bot.polling()