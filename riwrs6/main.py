import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import plotext as plt

def main():
    # Criação do dataframe com o arquivo JSON
    df = pd.read_json('alexandre_garcia.json')

    # Download de stopwords
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese')

    # Retirada de stopwords do título e conteúdo
    df['title'] = df['title'].apply(lambda x: ' '.join(word for word in x.split() if word not in stopwords))
    df['content'] = df['content'].apply(lambda x: ' '.join(word for word in x.split() if word not in stopwords))

    # Transformação de tabela
    vectorizer = CountVectorizer()

    XAG = vectorizer.fit_transform(df['content'])
    vocabulary = vectorizer.get_feature_names()
    pdXAG = pd.DataFrame(data=XAG.toarray(), columns=vocabulary)

    pdXAG = pdXAG.T

    # Soma de uso de palavras
    pdXAG['sum'] = pdXAG.sum(axis=1)

    # Ordenação decrescente do dataframe
    pdXAG.sort_values(by=['sum'], inplace=True, ascending=False)

    # Criação de bag of words e limpeza do dataframe
    bag_of_words = ['se', 'porque', 'sobre', 'ainda', 'mas', 'vai', 'não', 'no', 'os', 'ter', 'em',
                    'assim', 'bem', 'pode', 'na', 'cada', 'um']

    for word in bag_of_words:
        pdXAG.drop(word, axis=0, inplace=True)

    # Retirada de colunas sem utilidade
    pdXAG.drop(pdXAG.columns[0:87], axis=1, inplace=True)

    # Conversão das informações necessárias em listas
    indexes = pdXAG.index.tolist()
    values = pdXAG['sum'].tolist()

    #Plotagem do gráfico resultante
    plt.title('Frequência de palavras nos textos de Alexandre Garcia')
    plt.bar(indexes[:5], values[:5])
    plt.xlabel(values[:5])
    plt.show()


main()
