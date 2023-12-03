from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # pip install werkzeug==2.3.0
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# Definir caminho para upload e tipo de arquivo
UPLOAD_FOLDER = 'FlaskRifas/static/rifas'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Criar App
app = Flask (__name__)

# Configurar caminho do Banco de Dados
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///projetorifas.db'

# Chave de segurança
app.config['SECRET_KEY'] = '2d0b3351e6030061790922b0eb78d9b0ac2a89131b0e0915'

# Configurar Upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar Banco de Dados
database = SQLAlchemy(app)
migrate = Migrate(app, database)
# Criptografia
bcrypt = Bcrypt(app)

# Proteger Formulario
# csrf = CSRFProtect(app)

# Login
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='comprar'

from FlaskRifas.models import *

# with app.app_context():
#     database.create_all()

# Chamar as rotas
from FlaskRifas import routes

