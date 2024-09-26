import random, re, requests
import g4f
import g4f.Provider
from g4f.cookies import set_cookies

g4f.debug.logging = True
g4f.debug.version_check = False

cookie = "COLOQUE O COOKIE DO BING AQUI"
set_cookies(".bing.com", {
  "_U": cookie
})

def gerarImagem(prompt:str="", caminho:str=""):
  nome = "bg" + str(random.randrange(0, 100000))
  response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    provider=g4f.Provider.BingCreateImages,
    messages=[{"role":"user", "content": prompt}]
  )

  list_url = re.findall(r'src="([^"]+)"', response)
  if not list_url:
    list_url = re.findall(r'https?://\S+', response)
  
  url_anterior = ""
  for i, url in enumerate(list_url):
    result = url.split('?')[0]
    if result == url_anterior: continue
    image_response = requests.get(result)
    if image_response.status_code == 200:
      with open(f'{caminho}/{nome}_{i}.png', 'wb') as f:
        f.write(image_response.content)
      url_anterior = result
      print(f'Imagem {nome}_{i}.png salva com sucesso!')
    else:
      print(f'Não foi possível baixar a imagem {nome}\nURL: {result}')