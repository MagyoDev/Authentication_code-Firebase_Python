import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import bcrypt

# Add your Firebase credentials here
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-name.firebaseio.com/'
})

# Referência para o nó 'usuarios' no Realtime Database
ref_usuarios = db.reference('usuarios')

# Função para criar um novo usuário no banco de dados
def criar_usuario(email, senha):
    # Obtém todos os usuários do banco de dados
    usuarios = ref_usuarios.get()

    # Verifica se o usuário já existe
    if usuarios is not None and email.replace('.', '__dot__') in usuarios.keys():
        return False, 'O usuário já existe.'

    # Cria um novo usuário
    novo_usuario = {
        'email': email,
        'senha': bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }

    # Salva o novo usuário no banco de dados
    ref_usuarios.child(email.replace('.', '__dot__')).set(novo_usuario)

    return True, 'Usuário criado com sucesso.'

# Função para autenticar o usuário
def autenticar_usuario(email, senha):
    # Verifica se o usuário existe no banco de dados
    usuarios = ref_usuarios.get()
    if usuarios is not None and email.replace('.', '__dot__') in usuarios:
        usuario = usuarios[email.replace('.', '__dot__')]

        # Verifica se a senha está correta
        if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
            return True, 'Usuário autenticado com sucesso.', usuario['email']

    return False, 'Falha na autenticação: Email ou senha incorretos.', None

# Função para trocar a senha do usuário
def trocar_senha_usuario(email, senha_antiga, senha_nova):
    # Verifica se o usuário existe no banco de dados
    usuarios = ref_usuarios.get()
    if usuarios is not None and email.replace('.', '__dot__') in usuarios:
        usuario = usuarios[email.replace('.', '__dot__')]

        # Verifica se a senha antiga está correta
        if bcrypt.checkpw(senha_antiga.encode('utf-8'), usuario['senha'].encode('utf-8')):
            # Atualiza a senha do usuário
            nova_senha = bcrypt.hashpw(senha_nova.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ref_usuarios.child(email.replace('.', '__dot__')).update({'senha': nova_senha})
            return True, 'Senha atualizada com sucesso.'
        else:
            return False, 'Senha antiga incorreta.'
    else:
        return False, 'Usuário não encontrado.'
