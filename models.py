from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Companhia(Base):
    __tablename__ = "companhias"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    viagens = relationship("Voo", back_populates="companhia")

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"ID: {self.id} - COMPANHIA: {self.nome}"


class Voo(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)
    horario = Column(Integer, nullable=False)

    companhia_id = Column(Integer, ForeignKey("companhias.id"))
    companhia = relationship("Companhia", back_populates="viagens")

    def __init__(self, destino, horario, companhia):
        self.destino = destino
        self.horario = horario
        self.companhia = companhia

    def __repr__(self):
        return f"ID: {self.id} - DESTINO: {self.destino} - COMPANHIA: {self.companhia.nome}"

engine = create_engine("sqlite:///ViageFacil.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#cadastro de empresa e viagem
def cadastrar_empresa():
    with Session() as session:
        try:
            nome_empresa = input("Digite o nome da empresa: ").capitalize()
            empresa = Companhia(nome=nome_empresa)
            session.add(empresa)
            session.commit()
            print(f"Empresa {nome_empresa} cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def cadastrar_viagem():
    with Session() as session:
        try:
            destino = input("Digite o destino: ").capitalize()
            empresa = session.query(Companhia).filter_by(nome=destino).first()
            if empresa == None:
                print(f"Nenhum voo encontrado com esse nome {destino}")
                return
            else:
                companhias = input("Digite o nome da companhia para cadastrar").capitalize()
                companhia = session.query(Companhia).filter_by(nome=companhias).first()
                if companhia == None:
                    print(f"Nenhuma companhia cadastrada com esse nome {companhias}")
                    return
                else:
                    companhia.empresa.append(empresa)
                    session.commit()
                    print(f"Viagem {destino} registrada com sucesso na companhia {companhias}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

