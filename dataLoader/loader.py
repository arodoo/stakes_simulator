import pandas as pd
from sqlalchemy import text
from ..database import get_engine

# 1. Conexión usando el módulo centralizado de base de datos
engine = get_engine()

# 2. Lectura de archivos
map_df      = pd.read_excel("../share/map.xlsx")
center_df   = pd.read_excel("../share/centerpos2x.xlsx")
bamboo_df   = pd.read_excel("../share/bamboopattern.xlsx")
large_df    = pd.read_excel("../share/largescreenpixelpos.xlsx")

# 3. Carga dentro de una sola transacción
with engine.begin() as conn:               # ¡ATÓMICO!
    conn.execute(text("SET foreign_key_checks = 0;"))
    map_df.to_sql("map", conn, if_exists="append", index=False, chunksize=5000)
    center_df.to_sql("centerpos2x", conn, if_exists="append", index=False, chunksize=5000)
    bamboo_df.to_sql("bamboopattern", conn, if_exists="append", index=False, chunksize=5000)
    large_df.to_sql("largescreenpixelpos", conn, if_exists="append", index=False, chunksize=5000)
    conn.execute(text("SET foreign_key_checks = 1;"))

print("Carga completada sin pérdidas.")
