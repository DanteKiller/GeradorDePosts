import json, random, glob, os, unicodedata, re, shutil
from time import sleep
import ia

TITLEQTDE = 30
TEXTQTDE = 32
TEXTROW = 14

# Caminho das pastas
caminho_font = './font/VERDANA.TTF'
caminho_img_gerada = './post/imagens_gerada'
caminho_img_usada = './post/imagem_usada'
caminho_texto = './post/texto'
caminho_pronto = './post/pronto'

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
  text = re.sub(r'[{}]', '', request)
  text = text.replace("\n", " ")
  return "{" + text + "}"

def gerarImagem(nicho:str=""):
  prompt = f"Projete uma imagem de fundo com elementos relacionados a {nicho}, com foco na legibilidade quando o texto branco é sobreposto. Integre fractais abstratos ao fundo para adicionar profundidade à cena. Certifique-se de que as cores utilizadas permita que o texto branco se destaque claramente do fundo. A imagem não deve conter nenhum texto."
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
        temp = c + " "
  if not temp == "":
    conteudo += temp[:-1]
  return conteudo

def main(nicho:str=""):
  imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]
  if len(imgs) < 1:
    print("Gerando imagem")
    gerarImagem(nicho)
    imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]
  
  print("Gerando prompt")
  prompt = gerarPrompt(nicho)
  print("Salvando prompt")
  with open(f'./conteudo.txt', "w", encoding="UTF-8") as f:
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
  img = imgs[0]
  
  nome = "Post_" + str(random.randrange(0,100000))

  print("Salvando texto")
  with open(f'{caminho_texto}/{nome}.txt', "w", encoding="UTF-8") as f:
    f.write(title + "\n" + content + "\n" + description + "\n" + hashtag)

main("Saúde")