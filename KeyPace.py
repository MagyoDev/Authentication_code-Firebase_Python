from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

from database import criar_usuario, autenticar_usuario, trocar_senha_usuario

Window.size = (350, 580)

class KeyPaceApp(MDApp):
    email_autenticado = None

    def build(self):
        self.theme_cls.primary_palette = "Red"
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("screens/welcome.kv"))  # Carrega o arquivo KV da tela de boas-vindas
        sm.add_widget(Builder.load_file("screens/login.kv"))  # Carrega o arquivo KV da tela de login
        sm.add_widget(Builder.load_file("screens/signup.kv"))  # Carrega o arquivo KV da tela de cadastro
        sm.add_widget(Builder.load_file("screens/home.kv"))  # Carrega o arquivo KV da tela de home
        sm.add_widget(Builder.load_file("screens/qmsomos.kv"))  # Carrega o arquivo KV da tela de quem somos
        sm.add_widget(Builder.load_file("screens/info.kv"))  # Carrega o arquivo KV da tela de trocar informações
        return sm

    def on_start(self):
        Clock.schedule_once(self.login, 5)  # Agendando a transição para a tela de login após 5 segundos

    def login(self, *args):
        self.root.current = "login"  # Define a tela atual como a tela de login

    def home(self, *args):
        self.root.current = "home"  # Define a tela atual como a tela de home

    def logout(self):
        self.root.current = "login"

    def cadastrar(self, email, senha):
        sucesso, mensagem = criar_usuario(email, senha)  # Chama a função para cadastrar o usuário
        if sucesso:
            print(f"Usuário cadastrado com sucesso. Email: {email}")
            tela_cadastro = self.root.get_screen("signup")  # Obtém a referência à tela de cadastro
            tela_cadastro.ids.email_field.text = ""  # Limpa o campo de e-mail
            tela_cadastro.ids.password_field.text = ""  # Limpa o campo de senha
            self.root.current = "login"  # Volta para a tela de login
        else:
            print(f"Erro ao cadastrar usuário: {mensagem}")

    def autenticar(self, email, senha):
        sucesso, mensagem, email_autenticado = autenticar_usuario(email, senha)
        if sucesso:
            print(f"Usuário autenticado com sucesso. Email: {email_autenticado}")
            self.email_autenticado = email_autenticado  # Atualiza o valor da variável email_autenticado
            self.root.current = "home"  # Redireciona para a tela "home"
            tela_login = self.root.get_screen("login")  # Obtém a referência à tela de login
            tela_login.ids.email_field.text = ""  # Limpa o campo de e-mail
            tela_login.ids.password_field.text = ""  # Limpa o campo de senha
        else:
            print(f"Falha na autenticação: {mensagem}")

    def open_about_us_dialog(self):
        self.root.current = "quem_somos"

    def goto_home(self):
        self.root.current = "home"

    def trocar_senha(self, email, senha_antiga, senha_nova):
        sucesso, mensagem = trocar_senha_usuario(email, senha_antiga, senha_nova)
        if sucesso:
            print("Senha trocada com sucesso.")
            self.root.current = "home"  # Redireciona para a tela "home"
        else:
            print(f"Erro ao trocar a senha: {mensagem}")

    def open_info_dialog(self):
        self.root.current = "info"


# Executa o aplicativo
if __name__ == "__main__":
    KeyPaceApp().run()
