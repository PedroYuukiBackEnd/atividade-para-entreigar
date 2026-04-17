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
    cnpj = Column(String, nullable=False, unique=True)

    viagens = relationship("Voo", back_populates="companhia")

    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj

    def __repr__(self):
        return f"ID: {self.id} - COMPANHIA: {self.nome} - CNPJ: {self.cnpj}"


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


#----------------------------------------------------------
# BANCO
#----------------------------------------------------------
engine = create_engine("sqlite:///ViageFacil.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


#----------------------------------------------------------
# CADASTRAR EMPRESA
#----------------------------------------------------------
def cadastrar_empresa():
    with Session() as session:
        try:
            nome_empresa = input("Digite o nome da empresa: ").capitalize()
            cnpj = input("Digite o CNPJ: ")

            empresa = Companhia(nome=nome_empresa, cnpj=cnpj)

            session.add(empresa)
            session.commit()

            print(f"Empresa {nome_empresa} cadastrada com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")


#----------------------------------------------------------
# CADASTRAR VIAGEM
#----------------------------------------------------------
def cadastrar_viagem():
    with Session() as session:
        try:
            destino = input("Destino: ").capitalize()
            horario = int(input("Horário (ex: 14): "))

            companhias = session.query(Companhia).all()
            for c in companhias:
                print(f"{c.id} - {c.nome} - CNPJ: {c.cnpj}")

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
            print(f"\n--- {companhia.nome} ({companhia.cnpj}) ---")
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
# ATUALIZAR EMPRESA
#----------------------------------------------------------
def atualizar_empresa():
    with Session() as session:
        try:
            id_empresa = int(input("ID da empresa: "))
            empresa = session.get(Companhia, id_empresa)

            if not empresa:
                print("Empresa não encontrada!")
                return

            novo_nome = input("Novo nome: ").capitalize()
            novo_cnpj = input("Novo CNPJ: ")

            empresa.nome = novo_nome
            empresa.cnpj = novo_cnpj

            session.commit()
            print("Empresa atualizada com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")


#----------------------------------------------------------
# ATUALIZAR VIAGEM
#----------------------------------------------------------
def atualizar_viagem():
    with Session() as session:
        try:
            id_voo = int(input("ID do voo: "))
            voo = session.get(Voo, id_voo)

            if not voo:
                print("Voo não encontrado!")
                return

            novo_destino = input("Novo destino: ").capitalize()
            novo_horario = int(input("Novo horário: "))

            voo.destino = novo_destino
            voo.horario = novo_horario

            session.commit()
            print("Voo atualizado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")


#----------------------------------------------------------
# DELETAR EMPRESA
#----------------------------------------------------------
def deletar_empresa():
    with Session() as session:
        try:
            id_empresa = int(input("ID da empresa: "))
            empresa = session.get(Companhia, id_empresa)

            if not empresa:
                print("Empresa não encontrada!")
                return

            session.delete(empresa)
            session.commit()

            print("Empresa deletada com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")


#----------------------------------------------------------
# DELETAR VIAGEM
#----------------------------------------------------------
def deletar_viagem():
    with Session() as session:
        try:
            id_voo = int(input("ID do voo: "))
            voo = session.get(Voo, id_voo)

            if not voo:
                print("Voo não encontrado!")
                return

            session.delete(voo)
            session.commit()

            print("Voo deletado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Erro: {erro}")
#----------------------------------------------------------
# MENU
#----------------------------------------------------------
print("\n -- MENU -- \n")
ask = input("\n - 1 - Empresas \n 2 - Viagens")
#----------------------------------------------------------
match ask:
    case "1":
        print("\n Página: Empresas/Companhias")
        ask_1 = input("1 - Cadastrar \n 2 - Listar \n 3 - Atualizar \n 4 - Deletar")
        match ask_1:
            case "1":
                cadastrar_empresa()
            case "2": 
                listar_companhias()
            case "3":
                atualizar_empresa()
            case "4":
                deletar_empresa()
#----------------------------------------------------------
    case "2": 
        print("\n Página: Viagens/Voos")
        ask_1 = input("1 - Cadastrar \n 2 - Listar \n 3 - Atualizar \n 4 - Deletar")
        match ask_1:
            case "1":
                cadastrar_viagem()
            case "2": 
                listar_viagens()
            case "3":
                atualizar_viagem()
            case "4":
                deletar_viagem()
#----------------------------------------------------------