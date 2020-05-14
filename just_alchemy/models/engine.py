from sqlalchemy import create_engine

engine = create_engine('sqlite:///base.db?'
                       'check_same_thread=False')
