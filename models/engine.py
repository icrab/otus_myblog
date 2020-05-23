from sqlalchemy import create_engine
from definitions import ROOT_DIR

engine = create_engine(f'sqlite:///{ROOT_DIR}/base.db?'
                       'check_same_thread=False')
