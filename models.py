from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
#----------------------------------------------------------
# CLASSE COMPANHIAS/EMPRESAS
#----------------------------------------------------------
class Companhia(Base):
    __tablename__ = "companhias"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    viagens = relationship("Voo", back_populates="companhia")

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"ID: {self.id} - COMPANHIA: {self.nome}"
#----------------------------------------------------------
# CLASSE VOOS
#----------------------------------------------------------
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
#----------------------------------------------------------
# CADASTRO EMPRESA
#----------------------------------------------------------
def cadastrar_empresa():
    with Session() as session:
        try:
            nome_empresa = input("Digite o nome da empresa: ").capitalize()
            empresa = Companhia(nome=nome_empresa)
            session.add(empresa)
            session.commit()
            print(f"Empresa {nome_empresa} cadastrada com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")
#----------------------------------------------------------
# CADASTRO VIAGEM
#----------------------------------------------------------
def cadastrar_viagem():
    with Session() as session:
        try:
            destino = input("Destino: ").capitalize()
            horario = int(input("Horário (ex: 14): "))

            companhias = session.query(Companhia).all()
            for c in companhias:
                print(f"{c.id} - {c.nome}")

            companhia_id = int(input("ID da companhia: "))
            companhia = session.get(Companhia, companhia_id)

            if not companhia:
                print("Companhia não encontrada!")
                return

            voo = Voo(destino=destino, horario=horario, companhia=companhia)
            session.add(voo)
            session.commit()

            print("Voo cadastrado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")
#----------------------------------------------------------
# LISTAR COMPANHIAS
#----------------------------------------------------------
def listar_companhias():
    with Session() as session:
        companhias = session.query(Companhia).all()

        for companhia in companhias:
            print(f"\n--- {companhia.nome} ---")
            for voo in companhia.viagens:
                print(f"Destino: {voo.destino} | Horário: {voo.horario}")
#----------------------------------------------------------
# LISTAR VIAGENS
#----------------------------------------------------------
def listar_viagens():
    with Session() as session:
        voos = session.query(Voo).all()

        for voo in voos:
            print(f"ID: {voo.id} | Destino: {voo.destino} | Companhia: {voo.companhia.nome}")
#----------------------------------------------------------

