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
        internacional = Companhia(nome="internacional")
        latam = Companhia(nome="latam")

        v1 = Voo("cracolandia", 13, companhia=azul)
        v2 = Voo("Canada", 15, companhia=gol)
        v3 = Voo("Japão", 13, companhia=internacional)
        v4 = Voo("Jamaica", 13, companhia=latam)
        v5 = Voo("Inglaterra", 13, companhia=internacional)
        v6 = Voo("Estaods Unidos", 13, companhia=internacional)
        v7 = Voo("Argentina", 13, companhia=gol)
        v8 = Voo("Portugal", 13, companhia=azul)
        v9 = Voo("Angola", 13, companhia=gol)
        v10 = Voo("France", 13, companhia=azul)

        session.add_all([gol, azul, internacional, latam, v1,v2,v3,v4,v5,v6,v7,v8,v9,v10]) 
        session.commit()

        print("Companhias e voos inseridos!")

    except Exception as erro:
        session.rollback()
        print(f"Ocorreu um erro: {erro}")