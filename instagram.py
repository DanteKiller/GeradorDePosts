import logging, os, json
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from PIL import Image

logger = logging.getLogger()
logging.basicConfig(filename="Log.txt", encoding="utf-8", level=logging.DEBUG)

user = "Digite seu Usuario/Email/Telefone"
password = "Digite sua senha"
file_session = "session.json"

def login():
  client = Client()

  if not os.path.isfile(file_session):
    json.dump({}, open(file_session, 'w'))
  
  session = client.load_settings(file_session)

  login_session = False
  login_password = False

  if session['uuids']:
    try:
      client.login(user, password)
      try:
        client.get_timeline_feed()
      except LoginRequired:
        logger.info("Session is invalid, you need to login with username and password")
        old_session = client.get_settings()
        client.set_settings({})
        client.set_uuids(old_session['uuids'])

        client.login(user, password)
      login_session = True
    except Exception as e:
      logger.info("Couldn't login user using session information: %s" % e)

  if not login_session:
    try:
      logger.info("Attemption to login with username and password. username: %s" % user)
      if client.login(user, password):
        login_password = True
    except Exception as e:
      logger.info("Couldn't login user using username and password: %s" % e)
  
  if not login_password and not login_session:
    raise Exception("Couldn't login user with either password or session")
  else:
    client.dump_settings(file_session)

  return client

def postarFoto(caminho_pronto:str="", caminho_texto:str="", nome:str=""):
  client = login()
  img = Image.open(f'{caminho_pronto}/{nome}.png')
  rgb_img = img.convert('RGB')
  img_convert = f'./{nome}.jpg'
  rgb_img.save(img_convert)
  texto = open(f'{caminho_texto}/{nome}.txt', 'r', encoding='UTF-8').readlines()
  caption = f'{texto[0]}\n{texto[2]}{texto[3]}'
  client.photo_upload(
    path=img_convert,
    caption=caption
  )
  print("Imagem postada com sucesso!")
  os.remove(img_convert)