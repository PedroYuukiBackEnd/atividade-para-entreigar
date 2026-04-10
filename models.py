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

with Session() as session:
    try:
        gol = Companhia(nome="Gol")
        azul = Companhia(nome="Azul")

        viagem1 = Voo("cracolandia", 13, companhia=azul)
        viagem2 = Voo("canada", 15, companhia=gol)

        session.add_all([gol, azul, viagem1, viagem2]) 
        session.commit()

        print("Companhias e voos inseridos!")

    except Exception as erro:
        session.rollback()
        print(f"Ocorreu um erro: {erro}")