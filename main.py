import json, random, glob, os, unicodedata, re, shutil, instagram
from time import sleep
import ia
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from fractions import Fraction

TITLEQTDE = 30
TEXTQTDE = 32
TEXTROW = 14

# Caminho das pastas
caminho_font = './font/VERDANA.TTF'
caminho_img_gerada = './post/imagens_gerada'
caminho_img_usada = './post/imagem_usada'
caminho_texto = './post/texto'
caminho_pronto = './post/pronto'
caminho_img_resize = './post/imagem_resize'

tipo = {
  "Vertical":[(1080, 1350), 60.0], #4:5
  "Quadrado":[(1080, 1080), 50.0], #1:1
  "Horizontal": [(1080, 566), 65.0], #1.91:1
  "Stories":[(1080, 1920), 55.0], #9:16 
  "IGTV":[(420, 654), 20.0] #1:1.55 Foto de capa
}

def gerarTexto(prompt:str="", nicho:str=""):
  while True:
    request = ia.gerarPost(prompt)
    try:
      _request = consertarPost(request)
      result = json.loads(_request)
      break
    except Exception as e:
      print("Erro: " + e.msg)
      sleep(5)
    
  title = result["titulo"]
  content = result["conteudo"]
  cs = content.split("#")
  content = cs[0]
  description = result["descricao"]
  ds = description.split("#")
  description = ds[0]
  try:
    hashtags = result["hashtag"].lower()
    hashtag = unicodedata.normalize("NFD", hashtags)
    hashtag = hashtag.encode("ascii", "ignore")
    hashtag = hashtag.decode("utf-8")
  except:
    hashtags = f"#{nicho.lower()}"
  return title, content, description, hashtag

def consertarPost(request:str=""):
  text = re.sub(r'[{}`]', '', request)
  text = text.replace("json", " ")
  text = text.replace("\n", " ")
  return "{" + text + "}"

def gerarImagem(nicho:str=""):
  prompt = f"Projete uma imagem de fundo com elementos relacionados a {nicho}, com foco na legibilidade quando com o branco a ser sobreposto. Integre fractais abstratos ao fundo para adicionar profundidade à cena. Certifique-se de que as cores utilizadas permita que a cor branca se destaque claramente do fundo. A imagem não deve conter nenhum texto ou letras."
  ia.gerarImagem(prompt, caminho_img_gerada)

def gerarPrompt(nicho:str=""):
  while True:
    request = ia.criarPrompt(nicho)
    try:
      _request = consertarPost(request)
      result = json.loads(_request)
      break
    except:
      sleep(5)
  prompt = result["prompt"]
  publico_alvo = result["publico_alvo"]
  return f"{prompt} - público alvo: {publico_alvo}"

def editarTexto(text:str="", tqtde:int=0) -> str:
  conteudo = ""
  temp = ""
  ponto = False
  ct = text.split(" ")
  for c in ct:
    nt = len(c)
    ap = len(temp)
    if c == "": continue
    final = c[len(c)-1:]
    if final == "." or final == "!" or final == "?":
      ponto = True
    if ap + nt < tqtde:
      if ponto:
        temp += c + "\n"
        conteudo += temp
        temp = ""
        ponto = False
      else:
        temp += c + " "
    else:
      conteudo += temp[:-1] + "\n"
      if ponto:
        conteudo += c + "\n"
        temp = ""
        ponto = False
      else:
        temp = c + " "
  if not temp == "":
    conteudo += temp[:-1]
  return conteudo

def geraImagemComTexto(img:str="", titulo:str="", conteudo:str="", hashtag:str="", nome:str="", tipoSel:float=50.0):
  imagem = None
  draw = None
  print("Adicionando o texto na imagem")
  bg = Image.open(img).convert('RGB')
  x = bg.width//2
  y = bg.height//2
  imagem = Image.new('RGBA', bg.size)
  draw = ImageDraw.Draw(imagem)
  fonte = ImageFont.truetype(caminho_font, tipoSel + 0.1)
  fonte1 = ImageFont.truetype(caminho_font, tipoSel)

  draw.multiline_text(xy=(x,y), text=titulo+"\n"+conteudo, font=fonte, stroke_width=2, stroke_fill="#ffff00", fill="#1A3442", anchor="mm", align="center")

  imagem = imagem.filter(ImageFilter.BoxBlur(7))
  bg.paste(imagem, imagem)

  draw = ImageDraw.Draw(bg)
  draw.text(xy=(x,y), text=titulo+"\n"+conteudo, fill="#ffffff", font=fonte1, stroke_width=2, stroke_fill="#000000", anchor="mm", align="center")

  print("Salvando a imagem final")
  bg.save(f'{caminho_pronto}/{nome}.png')
  bg.close()
  print("Imagem final pronta")

def crop_resize(image, size, ratio):
  w, h = image.size
  if w > ratio * h:
    x, y = (w - ratio * h) // 2,0
  else:
    x, y = 0, (h- w / ratio) // 2
  image = image.crop((x, y, w - x, h - y))

  if image.size > size:
    image.thumbnail(size, Image.Resampling.LANCZOS)
  else:
    image = image.resize(size, Image.Resampling.LANCZOS)
  return image

def resizeImage(img_file:str="", size:any=(0,0)):
  try:
    image = crop_resize(Image.open(img_file), size, Fraction(*size))
    image_name = os.path.basename(img_file)
    image.save(f'{caminho_img_resize}/{image_name}')
    image.close()
    shutil.move(img_file, f'{caminho_img_usada}/{image_name}')
    return f'{caminho_img_resize}/{image_name}'
  except Exception as e:
    print(e)
    return None

def main(nicho:str="", tiponicho:str=""):
  imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]
  if len(imgs) < 1:
    print("Gerando imagem")
    gerarImagem(tiponicho)
    imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]

  tipoSel = tipo["Vertical"]
  img = resizeImage(imgs[0], tipoSel[0])
  if not img: return
  
  print("Gerando prompt")
  prompt = gerarPrompt(nicho)
  print("Salvando prompt")
  with open(f'./conteudo.txt', "a", encoding="UTF-8") as f:
    f.write(prompt + "\n")

  while True:
    print("Gerando o conteúdo")
    title, content, description, hashtag = gerarTexto(prompt, nicho)
    if len(title) == 0 or len(title) >= 60 or len(content) == 0 or len(content) > 500:
      sleep(3)
      continue
    break
  
  titulo = editarTexto(title, TITLEQTDE)
  conteudo = editarTexto(content, TEXTQTDE)
  
  # img = imgs[0]
  
  nome = "Post_" + str(random.randrange(0,100000))

  print("Salvando texto")
  with open(f'{caminho_texto}/{nome}.txt', "w", encoding="UTF-8") as f:
    f.write(title + "\n" + content + "\n" + description + "\n" + hashtag)

  print("Gerando imagem final")
  geraImagemComTexto(img, titulo, conteudo, hashtag, nome, tipoSel[1])

  # file_img = os.path.basename(img)
  # shutil.move(img, f'{caminho_img_usada}/{file_img}')

  print('Iniciando postagem')
  instagram.postarFoto(caminho_pronto, caminho_texto, nome)

  
def teste(tiponicho:str=""):
  imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]
  if len(imgs) < 1:
    print("Gerando imagem")
    gerarImagem(tiponicho)
    imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]

  tipoSel = tipo["Vertical"]
  img = resizeImage(imgs[0], tipoSel[0])
  if not img: return
  
  with open(f'{caminho_texto}/Post_43409.txt', "r", encoding="UTF-8") as f:
    textos = f.readlines()
    title = textos[0]
    content = textos[1].replace("\n", "")
    description = textos[2].replace("\n", "")
    hashtag = textos[3].replace("\n", "")
  
  titulo = editarTexto(title, TITLEQTDE)
  conteudo = editarTexto(content, TEXTQTDE)
    
  nome = "Post_" + str(random.randrange(0,100000))

  print("Gerando imagem final")
  geraImagemComTexto(img, titulo, conteudo, hashtag, nome, tipoSel[1])

main("Automação de post do instagram com nosso código", "python")
# teste("python")