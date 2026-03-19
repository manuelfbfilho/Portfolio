import numpy as np

def previsao_baseline(serie):
    historico = list(serie[-7:])
    previsoes = []

    for _ in range(30):
        p = np.mean(historico[-7:])
        previsoes.append(p)
        historico.append(p)

    return previsoes