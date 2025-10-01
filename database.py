# database.py

import os
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base, AnaliseContrato

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_tabelas():
    """Garante que as tabelas existam no banco de dados."""
    try:
        Base.metadata.create_all(bind=engine)
        # Mensagem removida para evitar repetições no console
    except Exception as e:
        print(f"Error creating database tables: {e}")

def salvar_analise(nome_arquivo: str, score: int, resumo: dict, analise_ia: str):
    """Salva uma análise de contrato no banco de dados."""
    db = SessionLocal()
    try:
        nova_analise = AnaliseContrato(
            nome_arquivo=nome_arquivo,
            score_risco=score,
            resumo_riscos=resumo,
            analise_completa_ia=analise_ia
        )
        db.add(nova_analise)
        db.commit()
        db.refresh(nova_analise)
        print(f"Análise para '{nome_arquivo}' salva com sucesso.")
        return nova_analise
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        db.rollback()
    finally:
        db.close()

def buscar_todas_analises():
    """Busca todas as análises salvas no banco, da mais recente para a mais antiga."""
    db = SessionLocal()
    try:
        analises = db.query(AnaliseContrato).order_by(desc(AnaliseContrato.id)).all()
        return analises
    finally:
        db.close()