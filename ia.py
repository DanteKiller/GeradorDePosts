import random, re, requests, os, config
import g4f
import g4f.Provider
from g4f.cookies import set_cookies

g4f.debug.logging = True
g4f.debug.version_check = False

cookie = config.COOKIE

set_cookies(".bing.com", {
  "_U": cookie
})

MODELO_PROMPT = """
{
  "prompt":"...",
  "publico_alvo":"..."
}
"""

PROMPT_CRIACAO = f"""
Você é um especialista em Criação de Prompt.
Você irá gerar as seguintes seções:
"
'Prompt': 'Forneça o melhor prompt possível de acordo com minha solicitação da forma mais específica, completa e direta'
'Público Alvo: 'Traga o público alvo para o meu nicho'
"
Um exemplo de prompt: "Você será um criador de conteúdo e criará um post sobre ... com bastante propriedade ..."
Pense cuidadosamente e use sua imaginação para criar um prompt incrível.
Quando eu falar "crie um prompt sobre ..." gere um prompt como sugerido acima sobre o nicho que irei solicitar.
A sua resposta deve ser retornado no formato json seguindo exatamente como o modelo:
{MODELO_PROMPT}
"""

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

def criarPrompt(nicho:str=""):
  prompt = "Não repita os mesmos abaixo:\n"
  with open(f'./conteudo.txt', "r", encoding="UTF-8") as f:
    text = f.read()
    prompt += text
  response = g4f.ChatCompletion.create(
    model=g4f.models.llama_3_1_70b,
    messages=[
      {"role": "system", "content": PROMPT_CRIACAO},
      {"role": "assistant", "content": "Entendi!"},
      {"role": "system", "content": prompt},
      {"role": "assistant", "content":"Entendi!"},
      {"role": "user", "content":f"crie um prompt sobre {nicho}"}
    ]
  )
  return response

MODELO ="""
{
  "titulo":"...",
  "conteudo": "...",
  "descricao":"...",
  "hashtag":"..."
}
"""

PROMPT_FINAL = f"""
Quando eu falar "Crie um Post" vc irá criar um Post com bastante engajamento.
O Post deve trazer informações importate que ajudará o público alvo sobre o assunto,
traga pontos importancias que dará informação ao público alvo.
No conteudo, adicione "Leia a descrição".
Na descrição entrege as informações necessárias para sanar as dúvidas sendo objetivo e claro.
Obs: O titulo de ter no máximo 50 caracteres, o conteudo deve conter no máximo 330 caracteres ao total, descricao deve conter no máximo 2000 caracteres ao total , no hashtag conter no mínimo 5 # para engajamento.
Não misture os conteúdos, título é em titulo, conteúdo é em conteudo, descrição é em descricao e hashtags é em hashtag.

O resultado deve ser em português.
A sua resposta deve ser retornado exatamente no formato json seguindo exatamente como o modelo:
{MODELO}
"""

def gerarPost(prompt:str="") -> str:
  response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[
      # {"role": "system", "content": prompt},
      # {"role": "user", "content": PROMPT_FINAL},
      # {"role": "assistant", "content": "Entendi!"},
      # {"role": "user", "content": "Crie um post"}
      {"role": "user", "content": f'Assunto: {prompt}\n{PROMPT_FINAL}\nCrie um Post'}
    ]
  )
  return response