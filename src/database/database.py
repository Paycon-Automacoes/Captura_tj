from FuncsForSPO.fpython.functions_for_py import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

engine = create_engine('sqlite:///bin/database.db', pool_size=15, max_overflow=20)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class TABLE(Base):
    __tablename__ = 'table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    n_processo = Column(String)
    status = Column(String)
    data_captura = Column(String)
    uf = Column(String)
    tipo = Column(String)
    personagem = Column(String)
    
    
Base.metadata.create_all(engine)  # cria a tabela no banco de dados

class DBManager:
    def __init__(self):
        # Inicializa uma nova sessão com o banco de dados.
        
        self.session = Session()
    def verify_if_n_processo_exists(self, n_processo):
        if self.session.query(TABLE).filter_by(n_processo=n_processo).first() is not None:
            return True
        else:
            return False
    
    def verify_if_n_processo_and_tipo_and_personagem_exists(self, n_processo, tipo, personagem):
        return self.session.query(TABLE).filter_by(n_processo=n_processo, tipo=tipo, personagem=personagem).first()
    def create_item(self, n_processo, status, data_captura, uf, tipo, personagem):
        # Cria um novo registro na tabela.
        if self.verify_if_n_processo_and_tipo_and_personagem_exists(n_processo, tipo, personagem) is not None:
            return True
        new_item = TABLE(n_processo=n_processo, status=status, data_captura=data_captura, uf=uf, tipo=tipo, personagem=personagem)
        self.session.add(new_item)
        self.session.commit()

    def get_item(self, id):
        # Retorna o registro com o ID fornecido
        return self.session.query(TABLE).filter_by(id=id).first()
    

    def delete_item(self, id):
        # Exclui o registro com o ID fornecido da tabela

        delete_item_from_db = self.get_item(id)
        self.session.delete(delete_item_from_db)
        self.session.commit()
        
    def delete_all(self):
        # Exclui todos os registros da tabela.

        self.session.query(TABLE).delete()
        self.session.commit()

    def get_item(self, id):
        # Retorna o registro com o ID fornecido da tabela. Se nenhum registro for encontrado, retorna None.
        return self.session.query(TABLE).filter_by(id=id).first()
    

    def get_column_status(self):
        # Retorna o registro de status com o ID fornecido da tabela. Se nenhum registro for encontrado, retorna None.
        return self.session.query(TABLE.status).all()
    
    

