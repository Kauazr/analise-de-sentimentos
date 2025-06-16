# ARQUIVO: treinar_modelo.py
"""
Script responsável por treinar o modelo de análise de sentimentos.

Ele usa uma base de frases pré-rotuladas, as transforma em um formato
numérico (vetorização) e treina um classificador Naive Bayes com esses dados.
Ao final, salva o modelo treinado e o vetorizador em arquivos .joblib para
que a aplicação principal possa carregá-los e usá-los para fazer novas previsões.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump

# --- Base de Dados de Treinamento ---
# Criei uma lista de frases de exemplo para treinar o modelo.
# Quanto mais variadas e realistas forem essas frases, melhor será o resultado.
frases = [
    # ---------------- POSITIVAS ----------------
    "Adorei o atendimento, voltarei com certeza!",
    "Meu cabelo ficou maravilhoso!",
    "Excelente serviço, muito satisfeita!",
    "Ótimo resultado, equipe muito profissional.",
    "Fui super bem atendida, recomendo muito!",
    "Corte perfeito, do jeitinho que pedi.",
    "Ambiente agradável e profissionais atenciosos.",
    "O produto deixou meu cabelo super macio!",
    "Minha escova ficou linda e durou dias.",
    "Super recomendo esse salão!",
    "Maravilhoso, me senti uma princesa!",
    "Gostei demais do tratamento.",
    "Tudo impecável, do início ao fim!",
    "Me explicaram tudo direitinho, super atenciosos.",
    "Hidratação potente, cabelo renovado!",
    "Resultado impecável, nota mil!",
    "Equipe carinhosa e super competente!",
    "Serviço de qualidade, preço justo.",
    "A coloração ficou perfeita!",
    "Meu cabelo nunca esteve tão bonito!",
    "Muito feliz com o resultado final.",
    "O cheiro do produto é ótimo!",
    "A escova progressiva ficou excelente.",
    "Atendimento rápido e eficiente.",
    "O corte foi exatamente como pedi.",
    "Me senti valorizada como cliente.",
    "A selagem deixou meu cabelo incrível!",
    "Fui muito bem recebida no salão.",
    "Me senti em casa, parabéns à equipe!",
    "Produtos de alta qualidade!",
    "A cabeleireira foi maravilhosa comigo.",
    "Amei a finalização do meu cabelo!",
    "Simplesmente perfeito!",
    "Fiquei encantada com o resultado.",
    "Voltarei com certeza!",
    "Saí do salão me sentindo renovada.",
    "Atendimento impecável!",
    "Fiquei extremamente satisfeita!",
    "O tratamento reconstrutor foi excelente.",
    "Meu cabelo ficou com um brilho lindo.",
    "A coloração combinou perfeitamente com meu tom de pele.",
    "Tudo foi feito com muito cuidado.",
    "Senti que realmente se importaram comigo.",
    "Fizeram milagres no meu cabelo!",
    "Nunca recebi tanta atenção em um salão.",
    "Satisfeita é pouco para definir meu sentimento!",
    "Um dos melhores atendimentos que já tive.",
    "Profissionais qualificados e simpáticos.",
    "Corte moderno, amei!",
    "Equipe gentil e serviço rápido.",
    "Cabelo leve, sedoso e com brilho.",
    "Coloração sem cheiro forte e com resultado lindo.",
    "Cabelo disciplinado e sem frizz. Perfeito!",
    "Meu cabelo ficou mais saudável após o procedimento.",
    "Gostei do atendimento",
    
    # ---------------- NEUTRAS ----------------
    "Foi tudo certo, mas nada demais.",
    "O atendimento foi normal.",
    "Achei o serviço ok.",
    "Esperava mais, mas não foi ruim.",
    "O resultado foi razoável.",
    "Corte básico, ficou como imaginei.",
    "Nada surpreendente, apenas o necessário.",
    "Foi uma experiência mediana.",
    "Ficou dentro do esperado.",
    "Não tenho do que reclamar, nem elogiar muito.",
    "Tudo foi feito, mas sem destaque.",
    "Serviço entregue como prometido.",
    "A tintura pegou bem, mas não foi incrível.",
    "O ambiente estava limpo, só isso.",
    "O corte não me surpreendeu.",
    "A escova foi comum.",
    "Resultado normal, como em qualquer salão.",
    "Funcionários educados, mas não muito simpáticos.",
    "Cabelo ficou aceitável.",
    "Tratamento leve, sem muitos efeitos.",
    "Experiência neutra.",
    "Nada que tenha me chamado a atenção.",
    "Serviço eficiente, sem mais.",
    "Atendimento decente.",
    "A profissional era correta.",
    "Ambiente organizado.",
    "Tive uma experiência tranquila.",
    "O tempo de espera foi ok.",
    "Tudo foi feito como planejado.",
    "Corte simétrico e neutro.",
    
    # ---------------- NEGATIVAS ----------------
    "Péssimo atendimento, saí chateada.",
    "O corte ficou horrível.",
    "Meu cabelo ficou ressecado depois do tratamento.",
    "Não gostei do resultado.",
    "Experiência ruim, não voltarei.",
    "Produto com cheiro muito forte e desagradável.",
    "Fiquei esperando muito tempo para ser atendida.",
    "A profissional foi grossa comigo.",
    "Meu cabelo ficou oleoso depois do tratamento.",
    "A selagem não funcionou.",
    "Saí pior do que entrei.",
    "A coloração ficou manchada.",
    "Muito caro para um serviço tão ruim.",
    "Meu couro cabeludo ficou irritado.",
    "Nada do que prometeram foi cumprido.",
    "Atendimento totalmente desorganizado.",
    "Não se preocuparam com minha opinião.",
    "Saí decepcionada com o serviço.",
    "Meu cabelo caiu muito após o uso do produto.",
    "Desperdicei meu dinheiro.",
    "Corte torto, malfeito.",
    "Cabelo com frizz e sem forma.",
    "O salão estava sujo.",
    "Ambiente barulhento e desconfortável.",
    "Fizeram algo que eu não pedi.",
    "Profissionais despreparados.",
    "A cor não fixou direito.",
    "Meu cabelo ficou duro depois da hidratação.",
    "O produto deixou meu cabelo pior.",
    "Muito tempo de espera, serviço ruim.",
    "Senti descaso com minha necessidade.",
    "A profissional parecia estar com pressa.",
    "Não recomendo esse salão a ninguém.",
    "Foi uma experiência frustrante.",
    "Nada ficou como eu pedi.",
    "Me senti mal atendida.",
    "Tudo muito desorganizado.",
    "O cheiro era insuportável.",
    "Cabelo ficou embaraçado e seco.",
    "Nunca mais volto aqui.",
    "Trataram meu cabelo sem cuidado.",
    "A tinta ardeu o meu couro cabeludo.",
    "Tive uma reação alérgica ao produto.",
    "Prometeram muito e não entregaram nada.",
    "Fui ignorada durante o atendimento.",
    "Não me senti valorizada.",
    "Corte completamente fora do padrão.",
    "Nenhuma técnica me passou confiança.",
    "Atendimento rude.",
    "A profissional errou na coloração.",
]

# --- Rótulos (Labels) ---
# Aqui eu defino o sentimento correspondente para cada frase da lista acima.
# A ordem e a quantidade de sentimentos devem ser exatamente as mesmas da lista de frases.
# 0 = Negativo | 1 = Neutro | 2 = Positivo
sentimentos = (
    [2] * 56 +  # 56 frases positivas
    [1] * 30 +  # 30 frases neutras
    [0] * 49    # 49 frases negativas
)

# --- Processo de Treinamento ---

# 1. Vetorização: Transformo as frases de texto em uma matriz de contagem de palavras.
# É assim que o modelo consegue "ler" as frases.
print("Vetorizando as frases...")
vetorizador = CountVectorizer()
X = vetorizador.fit_transform(frases)

# 2. Treinamento: Crio o classificador (escolhi o Multinomial Naive Bayes, que é bom para texto)
# e o treino com os dados vetorizados (X) e os sentimentos correspondentes (y).
print("Treinando o modelo Naive Bayes...")
modelo = MultinomialNB()
modelo.fit(X, sentimentos)

# 3. Salvamento: Salvo o modelo treinado e o vetorizador em disco.
# A aplicação principal vai carregar esses dois arquivos para fazer as previsões.
print("Salvando o modelo e o vetorizador em disco...")
dump(modelo, 'modelo_sentimentos.joblib')
dump(vetorizador, 'vetorizador.joblib')

print("\n✅ Modelo treinado e salvo com sucesso!")