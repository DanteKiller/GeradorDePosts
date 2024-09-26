import json, random, glob, os, unicodedata, re, shutil
from time import sleep
import ia

# Caminho das pastas
caminho_font = './font/VERDANA.TTF'
caminho_img_gerada = './post/imagens_gerada'
caminho_img_usada = './post/imagem_usada'
caminho_texto = './post/texto'
caminho_pronto = './post/pronto'

def gerarImagem(nicho:str=""):
  prompt = f"Projete uma imagem de fundo com elementos relacionados a {nicho}, com foco na legibilidade quando o texto branco é sobreposto. Integre fractais abstratos ao fundo para adicionar profundidade à cena. Certifique-se de que as cores utilizadas permita que o texto branco se destaque claramente do fundo. A imagem não deve conter nenhum texto."
  ia.gerarImagem(prompt, caminho_img_gerada)

def main(nicho:str=""):
  imgs = [x for x in glob.glob(rf"{caminho_img_gerada}/*.png")]
  if (len(imgs) < 1):
    print("Gerando imagem")
    gerarImagem(nicho)

main("Saúde")