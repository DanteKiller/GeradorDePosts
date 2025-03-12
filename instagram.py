import logging, os, json, config
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
from PIL import Image

logger = logging.getLogger()
logging.basicConfig(filename="Log.txt", encoding="utf-8", level=logging.DEBUG)

user = config.USUARIO
password = config.SENHA
LinkStories = config.LINK_STORIES
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

#NOVO
def convertPNGToJPG(img:list=[], caminho_img_jpg:str="", nome:str=""):
  imgs = []
  for i in img:
    imP = Image.open(i)
    rgb_im = imP.convert('RGB')
    im = i.split('_')[-1][:-4]
    rgb_im.save(f'{caminho_img_jpg}/{nome}_{im}.jpg')
    imgs.append(f'{caminho_img_jpg}/{nome}_{im}.jpg')
  imgs = sorted(imgs)
  return imgs

def postarFoto(caminho_pronto:str="", caminho_texto:str="", caminho_img_jpg:str="", nome:str=""):
  client = login()
  img_convert = convertPNGToJPG([f'{caminho_pronto}/{nome}.png'], caminho_img_jpg, nome)[0]
  texto = open(f'{caminho_texto}/{nome}.txt', 'r', encoding='UTF-8').readlines()
  caption = f'{texto[0]}\n{texto[2]}{texto[3]}'
  client.photo_upload(
    path=img_convert,
    caption=caption
  )
  print("Imagem postada com sucesso!")
  os.remove(img_convert)

def postarStories(images:list=[], caminho_img_jpg:str="", nome:str=""):
  client = login()
  imgs = convertPNGToJPG(images, caminho_img_jpg, nome)

  for img in imgs:
    client.photo_upload_to_story(
      path=img,
      links=[StoryLink(webUri=LinkStories)]
    )
    print("Stories postada com sucesso!")

def postarCarrocel(images:list=[], caminho_texto:str="", caminho_img_jpg:str="", nome:str=""):
  client = login()
  imgs = convertPNGToJPG(images, caminho_img_jpg, nome)
  texto = open(f'{caminho_texto}/{nome}.txt', "r", encoding="UTF-8").readlines()  
  caption = f'{texto[0]}\n{texto[2]}{texto[3]}'
  client.album_upload(
      paths=imgs,
      caption=caption
    )
  print("Carrocel postado com sucesso")
  for img in images:
    try:
      if len(images) > 0:
        os.remove(img)
    except:
      print("")