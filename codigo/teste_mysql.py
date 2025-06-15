# import mysql.connector # Comente ou remova esta linha
import pymysql # Adicione esta linha

print("--- Iniciando script teste_mysql.py (usando PyMySQL) ---")

try:
    print("Tentando conectar ao MySQL (usando PyMySQL)...")
    conn = pymysql.connect(  # Alterado aqui
        host="127.0.0.1",
        user="db_sentimentos",
        password="Db@senti",  # Use a mesma senha
        database="tb_sentimentos",
        connect_timeout=10, # PyMySQL também tem connect_timeout
        # Para PyMySQL, o controle de SSL é um pouco diferente,
        # mas para localhost geralmente não é necessário configurar explicitamente de início.
        # Se precisar de SSL com PyMySQL: cursorclass=pymysql.cursors.DictCursor, ssl={'ssl_disabled': True} ou outras opções.
        # Por enquanto, vamos tentar sem configurações de SSL explícitas com PyMySQL.
    )
    print("✔️ Conexão com o banco de dados bem-sucedida (PyMySQL)!")
    conn.close()
    print("Conexão fechada (PyMySQL).")
# except mysql.connector.Error as err: # Comente ou altere esta linha
except pymysql.Error as err:  # Alterado aqui
    print(f"❌ ERRO PyMySQL: {err}")
except Exception as e:
    print(f"❌ ERRO GERAL: {e}")
finally:
    print("--- Script finalizado (PyMySQL) ---")