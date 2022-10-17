import pandas as pd
from pymongo import MongoClient


def read_csv():
    try:
        df = pd.read_csv('world-happiness-report.csv')
        print('Arquivo CSV lido com sucesso!')
        return df
    except:
        print('Erro na leitura do arquivo CSV.')


def db_conn():
    try:
        ATLAS_URI = ''
        DB_NAME = ''
        COL_NAME = 'world-happiness-report'

        client = MongoClient(ATLAS_URI)
        selected_db = client[DB_NAME]
        selected_col = selected_db[COL_NAME]

        return selected_col
    except:
        print('\nErro de conexão ao banco de dados.')


def db_create_op():

    try:
        db_conn().insert_many(read_csv().to_dict('records'))
        print('Gravação finalizada com sucesso!')

    except:
        print('Erro de gravação')


def db_read_op(rows):
    cursor = db_conn().find()
    df = pd.DataFrame(list(cursor))
    df.drop('_id', inplace=True, axis=1)
    print(df.head(rows).to_string())


def main():
    title = 'Mackenzie - Coleta e armazenamento de dados'
    db = 'MongoDB'
    subtitle = 'Trilha 6'

    print('\n' + ' ' * round((80 - len(title))/2 - 1) + title)
    print('-' * 80)
    print(' ' * round((80 - len(subtitle))/2 - 1) + subtitle)
    print('-' * 80)
    print('Objetivo: \nRealizar a leitura de arquivo .CSV e a gravação em banco de dados de sua escolha\n')
    print('Banco de dados selecionado: ' + db)

    db_create_op()
    print('\n' + '-' * 80)

    print('Será realizada agora a leitura do banco de dados para comprovar a gravação.')
    rows = input('Informe quantas linhas deseja consultar: ')
    db_read_op(int(rows))


if __name__ == '__main__':
    main()

