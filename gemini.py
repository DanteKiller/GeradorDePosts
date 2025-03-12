import config
import google.generativeai as genai

api_key = config.API_KEY

genai.configure(api_key=api_key)

modelo_carrocel = """{
  "Título": "...!",
  "Apresentação": "... Mas antes não se esqueça de curtir e seguir nosso perfil para mais dicas",
  "Conteúdo": [{
      "1. ...": "...",
      "2. ...": "...",
      "3. ...": "..."
      }],
  "Hashtag": "..."
  }
"""

def gerarConteudo(nicho:str="", pergunta:str=""):
  prompt = f"""
  Você se passará por um criador de conteúdo para rede sociais sobre {nicho}.
  Você criará o conteúdo de acordo com a pergunta que irei fazer logo abaixo:
  "O post será sobre: {pergunta}".
  Com essas informações, quero que voce crie um post com bastante engajamento, 
  agregando os pontos importantes do assunto.
  O post deve incuir um gancho forte de dor ou desejo do meu público.
  Use títulos com gancho persuasivo que tenha um gatilho de curiosidade, exempo:
  "As 3 melhores dicas ..."
  "Vou te contar as 3 estratégias para ..."
  "Quando vc finalmente descobrir sobre essas 3 ..."

  Você irá buscar na internet e fará uma pesquisa profunda com um olhar de especialista,
  com análise no assunto perguntado e obter a melhor resposta posível.

  O modelo deve ser feito exatamente em json seguindo o exemplo acima:
  {modelo_carrocel}

  Seja o mais natural possível, como se estivesse conversando com o público, 
  adicione algumas perguntas ou algo que faça gerar engajamento e mais interação do público, 
  mas sem sair do foco do conteúdo.

  Título Inicial com até 50 caracteres de letras, a breve apresentação com até 200 caracteres de letras, 
  conteudo do assundo solicitado, cada um do conteúdo deve ter no minimo 100 letras e no máximo 400 letras, 
  minimo 5 hashtags para engajamento.
"""
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(prompt)
  result = response.text
  return result

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

def gerarPrompt(nicho:str=""):
  prompt = f"\n{PROMPT_CRIACAO}\n"
  prompt += "Não repita os mesmos abaixo:\n"
  with open(f'./conteudo.txt', "r", encoding="UTF-8") as f:
    text = f.read()
    prompt += text
  prompt += f"\ncrie um prompt sobre {nicho}"
  
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(prompt)
  result = response.text
  return result

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

def gerarPost(prompt:str=""):
  prompt_pronto = f'Assunto: {prompt}\n{PROMPT_FINAL}\nCrie um Post'
  
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(prompt_pronto)
  result = response.text
  return result