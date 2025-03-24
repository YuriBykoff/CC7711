import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MaxAbsScaler

def media(list_resultadoIteracao):
    media = sum(list_resultadoIteracao) / len(list_resultadoIteracao)
    media_str = 'Média: ' + str(media)

    return media_str

def desvioPadrao(list_resultadoIteracao):
    media = sum(list_resultadoIteracao) / len(list_resultadoIteracao)
    variancia = sum((x - media) ** 2 for x in list_resultadoIteracao) / len(list_resultadoIteracao)
    desvioPadrao_valor = math.sqrt(variancia)
    desvioPadrao_str = 'Desvio Padrão: ' + str(desvioPadrao_valor)

    return desvioPadrao_str
    
list_arquivosAnalisados = ['teste2', 'teste3', 'teste4', 'teste5']

for arquivoAnalisado in list_arquivosAnalisados:
    list_resultadoIteracao = []
    for iteracao in range(10):
        print('----' + arquivoAnalisado + '----')

        arquivo = np.load(arquivoAnalisado + '.npy')
        x = arquivo[0]

        scale= MaxAbsScaler().fit(arquivo[1])
        y = np.ravel(scale.transform(arquivo[1]))

        if arquivoAnalisado == 'teste2':
            iteracoes = 500

            regr = MLPRegressor(hidden_layer_sizes=(25,10),
                                max_iter=iteracoes,
                                activation='tanh', #{'identity', 'logistic', 'tanh', 'relu'},
                                solver='adam', #{‘lbfgs’, ‘sgd’, ‘adam’}
                                #loss_curve_ = 5, #se lbfgs
                                learning_rate = 'adaptive',
                                n_iter_no_change=iteracoes,
                                verbose=False)
            
        elif arquivoAnalisado == 'teste3':
            iteracoes = 900

            regr = MLPRegressor(hidden_layer_sizes=(30,20),
                                max_iter=iteracoes,
                                activation='tanh', #{'identity', 'logistic', 'tanh', 'relu'},
                                solver='adam', #{‘lbfgs’, ‘sgd’, ‘adam’}
                                #loss_curve_ = 5, #se lbfgs
                                learning_rate = 'adaptive',
                                n_iter_no_change=iteracoes,
                                verbose=False)
            
        elif arquivoAnalisado == 'teste4':
            iteracoes = 1700

            regr = MLPRegressor(hidden_layer_sizes=(40,25),
                                max_iter=iteracoes,
                                activation='tanh', #{'identity', 'logistic', 'tanh', 'relu'},
                                solver='adam', #{‘lbfgs’, ‘sgd’, ‘adam’}
                                #loss_curve_ = 5, #se lbfgs
                                learning_rate = 'adaptive',
                                n_iter_no_change=iteracoes,
                                verbose=False)
            
        elif arquivoAnalisado == 'teste5':
            iteracoes = 15000

            regr = MLPRegressor(hidden_layer_sizes=(300,200),
                                max_iter=iteracoes,
                                activation='tanh', #{'identity', 'logistic', 'tanh', 'relu'},
                                solver='adam', #{‘lbfgs’, ‘sgd’, ‘adam’}
                                #loss_curve_ = 5, #se lbfgs
                                learning_rate = 'adaptive',
                                n_iter_no_change=iteracoes,
                                verbose=False)

        #print('Treinando RNA')
        regr = regr.fit(x,y)

        #print('Preditor')
        y_est = regr.predict(x)

        plt.figure(figsize=[14,7])

        #plot curso original
        plt.subplot(1,3,1)
        plt.title('Função Original')
        plt.plot(x,y,color='green')

        #plot aprendizagem
        plt.subplot(1,3,2)
        plt.title('Curva erro (%s)' % str(round(regr.best_loss_,5)))
        plt.plot(regr.loss_curve_,color='red')
        print(regr.best_loss_)

        #plot regressor
        plt.subplot(1,3,3)
        plt.title('Função Original x Função aproximada')
        plt.plot(x,y,linewidth=1,color='green')
        plt.plot(x,y_est,linewidth=2,color='blue')
        plt.show()

        list_resultadoIteracao.append(regr.best_loss_)
        print(list_resultadoIteracao)
    
    media_str = media(list_resultadoIteracao)
    desvioPadrao_str = desvioPadrao(list_resultadoIteracao)
    print()
    print(media_str)
    print(desvioPadrao_str)