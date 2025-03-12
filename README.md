Instalar Ambiente Virtual: 
python -m venv venv

Bibliotecas: 
pip install -U g4f[all]

pip install pillow

pip install instagrapi

Site do Bing: 
https://www.bing.com/images/create

Clonar repositório e preparar ambiente virtual

No cmd digite: 
git clone https://github.com/DanteKiller/GeradorDePosts.git .

Obs: o "." é para clonar o repositório na raiz da pasta onde está o caminho no CMD, para uma subpasta, troque o ponto para o nome da pasta, exemplo: git clone https://github.com/DanteKiller/GeradorDePosts.git "GerarPosts"

Entre na pasta com o comando:
cd GeradorDePosts - caso tenha usado o . para clonar, ou o nome da pasta que você criou

Abra o VS Code usando o comando:
code .

No VS Code: 

instalar o ambiente virtual: 
python -m venv venv

Ativar ambiente virtual: 
venv\Scripts\Activate

Instalar requirements: 
pip install -r requirements.txt

PS: Alterar os dados no arquivo config.py
