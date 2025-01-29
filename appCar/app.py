from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config, db, migrate
from models.model_pessoa import Pessoa
from models.model_empresa import Empresa
from models.model_veiculo import Veiculo
from helpers import get_tipo_descricao,get_tipo_origem 
from routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    
    #  banco de dados e migrações
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registra as rotas
    app.register_blueprint(main_bp)
    
    # registra as funções do helper
    @app.context_processor
    def utility_processor():
        return dict(get_tipo_descricao=get_tipo_descricao , get_tipo_origem=get_tipo_origem)

    @app.before_request
    def create_tables():
        with app.app_context():
            db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
