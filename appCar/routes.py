import re
from config import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model_pessoa import Pessoa
from models.model_empresa import Empresa
from models.model_veiculo import Veiculo
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/cadastrarPessoa', methods=['GET', 'POST'])
def cadastrarPessoa():
    cnh_categorias = { 'A': request.form.get('cnh_categA'), 
                       'B': request.form.get('cnh_categB'),
                       'C': request.form.get('cnh_categC'), 
                       'D': request.form.get('cnh_categD'), 
                       'E': request.form.get('cnh_categE')
    }
    categorias_concatenadas = '|'.join([categoria for categoria, valor in cnh_categorias.items() if valor])  # Usado para ler dic e retorna lista concatena com pipe
    
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        cpf = re.sub(r'\D', '', cpf)  # Remover pontos e traços do CPF
        data_nascimento = request.form['data_nascimento']
        cnh_categ = categorias_concatenadas
        cnh = request.form['cnh'][:9]  # Garantir que o CNH tenha no máximo 9 caracteres
        data_vencimento_cnh = request.form['data_vencimento_cnh']
        cep  = request.form['cep']
        rua  = request.form['rua']
        numero  = request.form['numero']
        bairro  = request.form['bairro']
        cidade  = request.form['cidade']
        estado  = request.form['estado']
        email = request.form['email']
        telefone = request.form['telefone']
        
        pessoa_cpf = Pessoa.query.filter_by(cpf=cpf).first()
        pessoa_cnh = Pessoa.query.filter_by(cnh=cnh).first()
        
        if pessoa_cpf:
            flash('CPF já cadastrado. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('pessoa/cadastrarPessoa.html', 
                                   nome=nome, 
                                   cpf=cpf, 
                                   data_nascimento=data_nascimento,
                                   cnh_categ=cnh_categ, 
                                   cnh=cnh,
                                   data_vencimento_cnh=data_vencimento_cnh,
                                   cep=cep,
                                   rua=rua,
                                   numero=numero,
                                   bairro=bairro,
                                   cidade=cidade,
                                   estado=estado,
                                   email=email,
                                   telefone=telefone
                                   )
        elif pessoa_cnh:
            flash('CNH já cadastrada. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('pessoa/cadastrarPessoa.html',
                                   nome=nome, 
                                   cpf=cpf, 
                                   data_nascimento=data_nascimento,
                                   cnh_categ=cnh_categ, 
                                   cnh=cnh,
                                   data_vencimento_cnh=data_vencimento_cnh,
                                   cep=cep,
                                   rua=rua,
                                   numero=numero,
                                   bairro=bairro,
                                   cidade=cidade,
                                   estado=estado,
                                   email=email,
                                   telefone=telefone
                                   )
        else:
            nova_pessoa = Pessoa(
                nome=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                cnh_categ=cnh_categ,
                cnh=cnh,
                data_vencimento_cnh=data_vencimento_cnh,
                cep=cep,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                email=email,
                telefone=telefone
            )
            db.session.add(nova_pessoa)
            db.session.commit()
            flash('Pessoa cadastrada com sucesso!', 'success')
            return redirect(url_for('main.consultarPessoa'))
    
    return render_template('pessoa/cadastrarPessoa.html')

@main_bp.route('/consultarPessoa')
def consultarPessoa():
    pessoas = Pessoa.query.all()
    if not pessoas:
        flash('Não há dados', 'danger')
        return render_template('index.html')
    hoje = datetime.today().date()  # Data atual como datetime.date
    
    return render_template('pessoa/consultarPessoa.html', pessoas=pessoas, hoje=hoje)

@main_bp.route('/editarPessoa/<int:id>', methods=['GET', 'POST'])
def editarPessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    
    cnh_categorias = { 'A': request.form.get('cnh_categA'), 
                       'B': request.form.get('cnh_categB'),
                       'C': request.form.get('cnh_categC'), 
                       'D': request.form.get('cnh_categD'), 
                       'E': request.form.get('cnh_categE')
    }
    categorias_concatenadas = '-'.join([categoria for categoria, valor in cnh_categorias.items() if valor])
    
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.cpf = request.form['cpf']
        pessoa.cpf = re.sub(r'\D', '', pessoa.cpf)  # Remover pontos e traços do CPF
        pessoa.data_nascimento = request.form['data_nascimento']
        pessoa.cnh_categ = categorias_concatenadas
        pessoa.cnh = request.form['cnh'][:9]  # Garantir que o CNH tenha no máximo 9 caracteres
        pessoa.data_vencimento_cnh = request.form['data_vencimento_cnh']
        db.session.commit()
        return redirect(url_for('main.consultarPessoa'))
    
    return render_template('pessoa/editarPessoa.html', pessoa=pessoa)

@main_bp.route('/deletarPessoa/<int:id>')
def deletarPessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    cpf = pessoa.cpf
    db.session.delete(pessoa)
    db.session.commit()
    flash(f'O CPF:{cpf} foi deletado com sucesso!', 'success')
    return redirect(url_for('main.consultarPessoa'))

@main_bp.route('/testar')
def testar():
    return render_template('pessoa/teste.html')

@main_bp.route('/resultado', methods=['GET', 'POST'])
def resultado():
    chek1 = request.form.get('nameA')
    chek2 = request.form.get('nameB')
    return render_template('pessoa/resultado.html', valor1=chek1, valor2=chek2)

@main_bp.route('/cadastrarEmpresa', methods=['GET', 'POST'])
def cadastrarEmpresa():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        cnpj = re.sub(r'\D', '', cnpj)  # Remover pontos e traços do CNPJ
        cep = request.form['cep']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        email = request.form['email']
        telefone = request.form['telefone']

        empresa_cnpj = Empresa.query.filter_by(cnpj=cnpj).first()

        if empresa_cnpj: 
            flash('CNPJ já cadastrado. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('empresa/cadastrarEmpresa.html', 
                                   nome=nome, 
                                   cnpj=cnpj, 
                                   cep=cep,
                                   rua=rua,
                                   numero=numero,
                                   bairro=bairro,
                                   cidade=cidade,
                                   estado=estado,
                                   email=email,
                                   telefone=telefone
                                   )
        else:
            nova_empresa = Empresa(
                nome=nome,
                cnpj=cnpj,
                cep=cep,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                email=email,
                telefone=telefone
            )
            db.session.add(nova_empresa)
            db.session.commit()
            flash('Empresa cadastrada com sucesso!', 'success')
            return redirect(url_for('main.consultarEmpresa'))

    return render_template('empresa/cadastrarEmpresa.html')


@main_bp.route('/consultarEmpresa')
def consultarEmpresa():
    empresas = Empresa.query.all()
    if not empresas:
        flash('Não há dados', 'danger')
        return render_template('index.html')
    hoje = datetime.today().date()  # Data atual como datetime.date
    
    return render_template('empresa/consultarEmpresa.html', empresas=empresas, hoje=hoje)



@main_bp.route('/editarEmpresa/<int:id>', methods=['GET', 'POST'])
def editarEmpresa(id):
    empresa = Empresa.query.get_or_404(id)      
    if request.method == 'POST':
        empresa.nome = request.form['nome']
        empresa.cnpj = request.form['cnpj']
        empresa.cnpj = re.sub(r'\D', '', empresa.cnpj)  # Remover pontos e traços do CPF
        empresa.cep = request.form['cep']
        empresa.rua =  request.form['rua']
        empresa.estado = request.form['estado']
        empresa.cidade = request.form['cidade']
        empresa.numero = request.form['numero']
        empresa.bairro = request.form['bairro']
        empresa.email = request.form['email']
        empresa.telefone = request.form['telefone']
        db.session.commit()
        return redirect(url_for('main.consultarEmpresa'))
    
    return render_template('empresa/editarEmpresa.html', empresa=empresa)


@main_bp.route('/deletarEmpresa/<int:id>')
def deletarEmpresa(id):
    empresa = Empresa.query.get_or_404(id)
    cnpj = empresa.cnpj
    db.session.delete(empresa)
    db.session.commit()
    flash(f'O CNPJ:{cnpj} foi deletado com sucesso!', 'success')
    return redirect(url_for('main.consultarEmpresa'))






   
    # --------------------  Rotas Veiculos
    
@main_bp.route('/cadastrarVeiculo', methods=['GET', 'POST'])
def cadastrarVeiculo():
    if request.method == 'POST':
        tipo = int(request.form['tipo'])
        marca = request.form['marca']
        modelo = request.form['modelo'] 
        renavam = request.form['renavam']
        placa = request.form['placa']
        chassis = request.form['chassis']
        proprio =int(request.form['proprio'])
        licenciamento = request.form['licenciamento']
        ipva = request.form['ipva']
        observacao_carro = request.form['observacao_carro']
        
       
        veiculo_placa = Veiculo.query.filter_by(placa=placa).first()
        veiculo_renavam = Veiculo.query.filter_by(renavam=renavam).first()
        veiculo_chassis = Veiculo.query.filter_by(chassis=chassis).first()

      
        if veiculo_placa:
            flash('Placa já cadastrada. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('veiculo/cadastrarVeiculo.html', 
                                   tipo=tipo, 
                                   marca=marca, 
                                   modelo=modelo,
                                   renavam=renavam,
                                   placa=placa,
                                   chassis=chassis,
                                   proprio=proprio,
                                   licenciamento=licenciamento,
                                   ipva=ipva,
                                   observacao_carro=observacao_carro)

        if veiculo_renavam:
            flash('Renavam já cadastrado. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('veiculo/cadastrarVeiculo.html', 
                                   tipo=tipo, 
                                   marca=marca, 
                                   modelo=modelo,
                                   renavam=renavam,
                                   placa=placa,
                                   chassis=chassis,
                                   proprio=proprio,
                                   licenciamento=licenciamento,
                                   ipva=ipva,
                                   observacao_carro=observacao_carro)
                                   
        if veiculo_chassis:
            flash('Chassis já cadastrado. Por favor, verifique o número e tente novamente.', 'danger')
            return render_template('veiculo/cadastrarVeiculo.html', 
                                   tipo=tipo, 
                                   marca=marca, 
                                   modelo=modelo,
                                   renavam=renavam,
                                   placa=placa,
                                   chassis=chassis,
                                   proprio=proprio,
                                   licenciamento=licenciamento,
                                   ipva=ipva,
                                   observacao_carro=observacao_carro)                        

        # Se todos os checks passarem, adiciona o novo veículo
        novo_veiculo = Veiculo(
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            renavam=renavam,
            placa=placa,
            chassis=chassis,
            proprio=proprio,
            licenciamento=licenciamento,
            ipva=ipva,
            observacao_carro=observacao_carro
        )
        db.session.add(novo_veiculo)
        db.session.commit()
        flash('Veículo cadastrado com sucesso!', 'success')
        return redirect(url_for('main.consultarVeiculo'))

    return render_template('veiculo/cadastrarVeiculo.html')


@main_bp.route('/consultarVeiculo')
def consultarVeiculo():
    veiculos = Veiculo.query.all()
    if not veiculos:
        flash('Não há dados', 'danger')
        return render_template('index.html')
    hoje = datetime.today().date()  # Data atual como datetime.date
    
    return render_template('veiculo/consultarVeiculo.html', veiculos=veiculos, hoje=hoje)



@main_bp.route('/editarVeiculo/<int:id>', methods=['GET', 'POST'])
def editarVeiculo(id):
    veiculo = Veiculo.query.get_or_404(id)      
    if request.method == 'POST':
       veiculo.tipo = int(request.form['tipo'])
       veiculo.marca = request.form['marca']
       veiculo.modelo = request.form['modelo'] 
       veiculo.renavam = request.form['renavam']
       veiculo.placa = request.form['placa']
       veiculo.chassis = request.form['chassis']
       veiculo.proprio =int(request.form['proprio'])
       veiculo.licenciamento = request.form['licenciamento']
       veiculo.ipva = request.form['ipva']
       veiculo.observacao_carro = request.form['observacao_carro']
       db.session.commit()
       return redirect(url_for('main.consultarVeiculo'))
    
    return render_template('veiculo/editarVeiculo.html', veiculo=veiculo)




@main_bp.route('/deletarVeiculo/<int:id>')
def deletarVeiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    placa = veiculo.placa
    db.session.delete(veiculo)
    db.session.commit()
    flash(f'A Placa:{placa} foi deletada com sucesso!', 'success')
    return redirect(url_for('main.consultarVeiculo'))