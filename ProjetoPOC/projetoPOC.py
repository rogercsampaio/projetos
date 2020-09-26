
# coding: utf-8

# # Projeto: Prever Insuficiência Cardíaca baseado em fatores clínicos e comportamentais

# A Insuficiência Cardíaca (causada por doenças cardiovasculares) é a principal
# causa de morte de vidas todos os anos, representando um percentual de 31% de todas as mortes mundiais. Este conjunto de dados contém doze características divididas em fatores clínicos e comportamentais como, por exemplo, nível de plaquetas e sódio sérico no sangue, fumante ou não, hipertenso ou não e pode ser utilizado para prever a mortalidade por doenças cardiovasculares. Objetivo do trabalho é realizar uma análise exploratória sobre o conjunto de dados e descobrir uma série de insights para auxiliar a equipe médica para a tomada de ações preventivas.

# In[272]:


# 1 - Instale o pacote 'squarify' caso não possua
#!pip install squarify

# 2 - Importação de pacotes e bibliotecas necessárias
# Pré-processamento
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify 
import requests 
import io
import numpy as np
from sklearn.preprocessing import StandardScaler

# Treinamento e teste
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# Algoritmos de Machine Learning
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

from sklearn.metrics import confusion_matrix

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


link = 'https://raw.githubusercontent.com/rogercsampaio/projetos/master/ProjetoPOC/datasets/heart_failure_clinical_records_dataset.csv'
s = requests.get(link).text


# In[3]:


# 2 - Importando os dados para o dataset
# heart_failure_clinical_records_dataset.csv
dadosClinicos = pd.read_csv(io.StringIO(s))


# In[4]:


# Visualizando os primeiros registros e tipos de dados
dadosClinicos.head()


# In[5]:


print(type(dadosClinicos))


# In[6]:


dadosClinicos.dtypes


# In[7]:


dadosClinicos


# In[8]:


# Ajustando os tipos de dados, renomeando colunas.


# In[9]:


dadosClinicos.age = dadosClinicos.age.astype(int)


# In[10]:


dadosClinicos.anaemia = dadosClinicos.anaemia.astype(bool)


# In[11]:


dadosClinicos.diabetes = dadosClinicos.diabetes.astype(bool)


# In[12]:


dadosClinicos.high_blood_pressure = dadosClinicos.high_blood_pressure.astype(bool)


# In[13]:


dadosClinicos['sex'] = dadosClinicos['sex'].replace(0, 'F')


# In[14]:


dadosClinicos['sex'] = dadosClinicos['sex'].replace(1, 'M')


# In[15]:


dadosClinicos.sex = dadosClinicos.sex.astype(str)


# In[16]:


type(dadosClinicos.sex)


# In[17]:


dadosClinicos.smoking = dadosClinicos.smoking.astype(bool)


# In[18]:


# paciente falheceu ou não durante o evento
dadosClinicos.DEATH_EVENT = dadosClinicos.DEATH_EVENT.astype(bool) 


# In[19]:


dadosClinicos = dadosClinicos.rename(columns = {'DEATH_EVENT':'dieOrNot'}, inplace = False)


# In[20]:


dadosClinicos.columns


# In[21]:


# Verificação de valores Null (para a modelagem preditiva)
dadosClinicos.isnull().values.any()


# In[22]:


# 3 - Análise Exploratória
# Informações estatísticas gerais
# Para variáveis quantitativas (numéricas)
dadosClinicos.describe()


# In[23]:


# Número de linhas, colunas, tipo de cada dado
dadosClinicos.info()


# In[24]:


# Análise unilateral. Varíavel: age (quantitativa). Possível será CATEGÓRICA.
# Resumo estatístico básico
dadosClinicos.age.describe()


# In[25]:


plt.boxplot(dadosClinicos.age)
plt.title('Boxplot de idades')


# In[26]:


plt.hist(dadosClinicos.age)
plt.xlabel('Idades')
plt.ylabel('Frequência')
plt.title('Histograma de idades')


# In[27]:


# Exploração da varíavel categórica anaemia
# Resumo estástico básico
dadosClinicos.anaemia.describe()


# In[28]:


# Contagem de valores
dadosClinicos.anaemia.value_counts()


# In[29]:


labelsNomesAnemia = "Não tem anemia","Tem anemia"
plt.pie(dadosClinicos.anaemia.value_counts(),labels = labelsNomesAnemia, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de pacientes com anemia')


# In[30]:


plt.bar(labelsNomesAnemia,dadosClinicos.anaemia.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de pacientes com e sem anemia')


# In[31]:


# Exploração da varíavel creatinine_phosphokinase
# Resumo estástico básico
dadosClinicos.creatinine_phosphokinase.describe()


# In[32]:


plt.boxplot(dadosClinicos.creatinine_phosphokinase)
plt.title('Boxplot de creatinine_phosphokinase')
# Note que há bastante outliers, necessário ajustar para o modelo preditivo


# In[33]:


plt.hist(dadosClinicos.creatinine_phosphokinase,bins = 3)
plt.xlabel("Creatinine_phosphokinase")
plt.ylabel("Frequência")
plt.title("Histograma de creatinine_phosphokinase (CPK) no sangue")


# In[34]:


# Exploração da variável diabetes (categórica)
# Contagem de valores
dadosClinicos.diabetes.value_counts()


# In[35]:


labelsNomesDiabetes = "Não tem diabete","Tem diabete "
plt.pie(dadosClinicos.diabetes.value_counts(),labels = labelsNomesDiabetes, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de pacientes com diabetes')


# In[36]:


plt.bar(labelsNomesDiabetes,dadosClinicos.diabetes.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de pacientes sem e com diabete')


# In[37]:


# Exploração da varíavel ejection_fraction
# Resumo estástico rápido
dadosClinicos.ejection_fraction.describe()


# In[38]:


plt.boxplot(dadosClinicos.ejection_fraction)
plt.title('Boxplot de ejection_fraction')


# In[39]:


plt.hist(dadosClinicos.ejection_fraction)
plt.xlabel("ejection_fraction")
plt.ylabel("Frequência")
plt.title("Histograma de 'ejection_fraction'")


# In[40]:


# Exploração da variável 'high_blood_pressure' (categórica)


# In[41]:


# Contagem de valores
dadosClinicos.high_blood_pressure.value_counts()


# In[42]:


labelsNomesPressaoAlta = "Não tem pressão alta","Tem pressão alta "
plt.pie(dadosClinicos.high_blood_pressure.value_counts(),labels = labelsNomesPressaoAlta, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de pacientes com pressão alta')


# In[43]:


# Quantidade
plt.bar(labelsNomesPressaoAlta,dadosClinicos.high_blood_pressure.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de pacientes sem e com pressão alta')
# plt.hist(dadosClinicos.ejection_fraction, bins = 2) # não agrega muito


# In[44]:


# Exploração da varíavel platelets (quantitativa)
# Resumo estátistico breve
dadosClinicos.platelets.describe()


# In[45]:


plt.boxplot(dadosClinicos.platelets)
plt.title('Boxplot Plaquetas (mg/mL) no sangue')
# Note que há bastante outliers


# In[46]:


plt.hist(dadosClinicos.platelets)
plt.title('Histograma Plaquetas (mg/mL) no sangue')
plt.ylabel('Frequência')


# In[47]:


# Exploração variável quantitativa 'serum_creatinine' 
# Resumo estástico rápido
dadosClinicos.serum_creatinine.describe()


# In[48]:


plt.boxplot(dadosClinicos.serum_creatinine)
plt.title('Boxplot - Nível de creatinina sérica no sangue (mg / dL)')
# Há bastante valores outliers


# In[49]:


plt.hist(dadosClinicos.serum_creatinine)
plt.title('Histograma - Nível de creatinina sérica no sangue (mg / dL)')
plt.ylabel('Frequência')


# In[50]:


# Exploração da varíavel serum_sodium (quantitativa)
# Resumo estástico rápido
dadosClinicos.serum_sodium.describe()


# In[51]:


plt.boxplot(dadosClinicos.serum_sodium)
plt.title('Boxplot - Nível de sódio sérico no sangue (mEq / L)')


# In[52]:


plt.hist(dadosClinicos.serum_sodium)
plt.title('Histograma - Nível de sódio sérico no sangue (mEq / L)')
plt.ylabel('Frequência')


# In[53]:


# Exploração da varíavel sex (categórica)


# In[54]:


# Contagem de valores
dadosClinicos.sex.value_counts()


# In[55]:


labelsNomesSexo = "Masculino","Feminino"
plt.pie(dadosClinicos.sex.value_counts(),labels = labelsNomesSexo, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de sexo')


# In[56]:


# Quantidade
plt.bar(labelsNomesSexo,dadosClinicos.sex.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de sexo de pacientes')


# In[57]:


# Exploração da varíavel smoking (categórica)


# In[58]:


# Contagem de valores
dadosClinicos.smoking.value_counts()


# In[59]:


labelsNomesFumantesOuNao = "Não fuma","Fuma"
plt.pie(dadosClinicos.smoking.value_counts(),labels = labelsNomesFumantesOuNao, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de fumantes')


# In[60]:


# Quantidade
plt.bar(labelsNomesFumantesOuNao,dadosClinicos.smoking.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de fumantes')


# In[61]:


# Exploração da varíavel time representando número de dias (categórica)


# In[62]:


# Contagem de valores
dadosClinicos.time.describe()


# In[63]:


plt.boxplot(dadosClinicos.time)
plt.title('Boxplot - Período de acompanhamento em dias')


# In[64]:


plt.hist(dadosClinicos.time)
plt.title('Período de acompanhamento em dias')
plt.ylabel('Frequência')


# In[65]:


dadosClinicos.time


# In[66]:


# Exploração varíavel categórica dieOrNot


# In[67]:


dadosClinicos.dieOrNot.value_counts()


# In[68]:


labelsNomesMorteOuNao = "Não morreu","Morreu"
plt.pie(dadosClinicos.dieOrNot.value_counts(),labels = labelsNomesMorteOuNao, autopct='%1.1f%%', shadow = True)
plt.title('Porcentagem de Mortes')


# In[69]:


# Quantidade
plt.bar(labelsNomesMorteOuNao,dadosClinicos.dieOrNot.value_counts())
plt.ylabel('Quantidade')
plt.title('Quantidade de Mortes')


# In[70]:


# Análise multivariada (duas ou mais varíaveis). 
# Correlação entre variáveis. 
# Correlação varia entre -1 (correlação negativa: uma diminui, outra aumenta) a 1 (correlação positiva, ambas
# variáveis vão no mesmo sentido). Correlação identifica o relacionamento linear entre variáveis, o que 
# não significa causalidade.
# corr() = a correlação de Pearson
dadosClinicos.corr()


# In[71]:


# Gráfico de correlação
plt.figure(figsize=(10, 6))
sns.heatmap(dadosClinicos.corr(),
            annot = True,
            fmt = '.2f',
            cmap='Blues')
plt.title('Correlação entre variáveis do dataset de dadosClinicos')
plt.show()
# As correlação estão fracas, considere que boas seriam em torno de 70% ...


# In[72]:


# Análise: idade e nível de creatinine_phosphokinase     


# In[73]:


# Comprovando a correlação, por exemplo, entre age e creatinine_phosphokinase, que está muito fraca
plt.scatter(dadosClinicos.age,dadosClinicos.creatinine_phosphokinase)
plt.xlabel("Idade")
plt.ylabel("Nível creatinina sérica no sangue (mg / dL)")
plt.title('Relação Idade x Nível de creatinina sérica')


# In[74]:


# Análise: idade x nível de ejection_fraction
# Comprovando a correlação, por exemplo, entre age e ejection_fraction, que está muito fraca
plt.scatter(dadosClinicos.age,dadosClinicos.ejection_fraction)
plt.xlabel("Idade")
plt.ylabel("Nível de sódio sérico no sangue (mEq / L)")
plt.title("Nível de sódio sérico no sangue (mEq / L)")


# In[75]:


# Análise: idades x plaquetas
# Comprovando a correlação, por exemplo, entre age e plaquetas, que está muito fraca
plt.scatter(dadosClinicos.age,dadosClinicos.platelets)
plt.xlabel("Idade")
plt.ylabel("Plaquetas (mg/mL) no sangue)")
plt.title("Nível Plaquetas (mg/mL) no sangue por idade")


# In[76]:


# Análise: idades x serum_creatinine
# Comprovando a correlação, por exemplo, entre age e serum_creatinine, que está muito fraca
plt.scatter(dadosClinicos.age,dadosClinicos.serum_creatinine)
plt.xlabel("Idade")
plt.ylabel("Plaquetas (mg/mL) no sangue)")
plt.title("Nível serum_creatinine'enzima CPK' (mg/mL)  por idade")


# In[77]:


# Análise: idades x serum_sodium 
# Comprovando a correlação, por exemplo, entre age e serum_creatinine, que está muito fraca
plt.scatter(dadosClinicos.age,dadosClinicos.serum_sodium)
plt.xlabel("Idade")
plt.ylabel("Porcentagem de Serum_sodium no sangue")
plt.title("Nível serum_sodium por idade")


# In[78]:


# Contar quantos tem anaemia categorizando por sexo
anaemia_map = {0: 'Não tem', 1: 'Tem'}
sns.factorplot('anaemia',data = dadosClinicos, kind='count',hue = 'sex').set_xticklabels(anaemia_map.values())
plt.ylabel('Quantidade')
plt.xlabel('Anaemia')
plt.title('Contagem de Pacientes Anémicos por Sexo')


# In[79]:


# Contar quantos são diabéticos por sexo 
diabete_map = {0: 'Não tem', 1: 'Tem'}
sns.factorplot('diabetes',data = dadosClinicos, kind='count',hue = 'sex').set_xticklabels(diabete_map.values())
plt.ylabel('Quantidade')
plt.xlabel('Diabetes')
plt.title('Contagem de Pacientes Diabéticos por Sexo')


# In[80]:


# Contagem de Pacientes Fumantes por Sexo
fumantes_map = {0: 'Não é fumante', 1: 'É fumante'}
sns.factorplot('smoking',data = dadosClinicos, kind='count',hue = 'sex').set_xticklabels(fumantes_map.values())
plt.ylabel('Quantidade')
plt.xlabel('Fumantes')
plt.title('Contagem de Pacientes Fumantes por Sexo')


# In[81]:


# Contar quantos tem pressão alta por sexo
pressaoAltaouNao_map = {0: 'Não tem', 1: 'Tem pressão alta'}
sns.factorplot('high_blood_pressure',data = dadosClinicos, kind='count',hue = 'sex').set_xticklabels(pressaoAltaouNao_map.values())
plt.ylabel('Quantidade')
plt.xlabel('Pressão Alta')
plt.title('Contagem de Pacientes por Pressão Alta por Sexo')


# In[82]:


# Contar quantos morreram baseado no sexo
morreramOuNao_map = {0: 'Não faleceu', 1: 'Faleceu'}
sns.factorplot('dieOrNot',data = dadosClinicos, kind='count',hue = 'sex').set_xticklabels(morreramOuNao_map.values())
plt.ylabel('Quantidade')
plt.xlabel('Falecimentos')
plt.title('Contagem de Órbitos por Sexo')


# In[83]:


# Tempo médio de acompanhamento em dias por sexo (total)
tempoMediaAcompanhSexo = dadosClinicos.groupby(['sex']).mean()
squarify.plot(sizes=[tempoMediaAcompanhSexo.iloc[0].time,
                     tempoMediaAcompanhSexo.iloc[1].time], label=["Mulheres", "Homens"], 
              color=["red","green"], alpha=.2)
plt.title('Tempo Médio de Acompanhamento de Dias dos Pacientes')
plt.axis('off')
plt.show()
tempoMediaAcompanhSexo.time


# In[84]:


# Tempo de acompanhamento em dias por faixa de idade
valorMin = dadosClinicos.age.min()
valorMax = dadosClinicos.age.max()
divParte = (valorMax - valorMin)/3
squarify.plot(sizes=[len(dadosClinicos[dadosClinicos['age'].between(valorMin,valorMin+divParte)]),
                     len(dadosClinicos[dadosClinicos['age'].between(valorMin+divParte,valorMin+(divParte*2))]),
                     len(dadosClinicos[dadosClinicos['age'].between(valorMin+(divParte*2),valorMax)])
                    ], 
              label=["Faixa etária 1 idade: %d a %d" %(valorMin,valorMin+divParte), 
                     "Faixa etária 2 idade: %d a %d" %(valorMin+divParte,valorMin+(divParte*2)),
                     "Faixa etária 3 idade: %d a %d" %(valorMin+(divParte*2),valorMax)], 
              color=["red","green","yellow"], alpha=.3)
plt.title('Tempo Médio de Acompanhamento de Dias dos Pacientes por Faixa Etária')
plt.axis('off')
plt.show()


# ### Pré-processamento

# #### Aplicação de padronização, para que os dados tenham uma distribuição normal, com média = 0, desvio padrão = 1. Técnica aplicável somente em VARIÁVEIS QUANTITATIVAS, necessário para alguns algortimos de Machine Learning.

# In[103]:


# Transformar o dataset para um objeto numpy (vetor)
dadosClinicosArray = dadosClinicos.values


# In[104]:


dadosClinicosArray


# In[105]:


# Divisão entre variáveis PREDITORAS e TARGET
dadosClinicosPreditoras = dadosClinicos.iloc[:,0:12]
dadosClinicosTarget = dadosClinicos.iloc[:,12];


# In[109]:


dadosClinicosPreditoras.head()


# In[108]:


dadosClinicosTarget.head()


# In[136]:


# Criando os conjuntos de dados de treino e de teste
X_treino, X_teste, Y_treino, Y_teste = train_test_split(dadosClinicosPreditoras,dadosClinicosTarget, 
                                                        test_size = 0.30)


# In[148]:


# Transformar o dataset para um objeto numpy (vetor)
dadosClinicosArrayX = X_treino.values


# In[149]:


# Aplicando a PADRONIZAÇÃO somente a X_treino
# Gerando o novo padrão
scaler = StandardScaler().fit(dadosClinicosArrayX)
standardX = scaler.transform(dadosClinicosArrayX)


# In[150]:


# Sumarizando os dados transformados
print("Dados Originais: \n\n", dadosClinicos.values)
print("\n Dados Padronizados: \n\n", standardX[0:5,:])


# In[151]:


# Comprovando que estamos diante de uma distribuição normal
plt.hist(standardX)
print('Media %f' %standardX.mean())
print('Desvio padrão %d ' %np.std(standardX))


# In[ ]:


# Agora com os dados padronizados, temos a possibilidade de usá-lo na construção do MODELO PREDTIVO.


# ## Aplicação do Machine Learning 

# In[88]:


# Construindo o modelo preditivo (problema de classificação: morte ou não)


# #### Sem padronizar os dados de treino.

# In[124]:


# 1 - Algoritmo LogisticRegression
modeloLogicR = LogisticRegression()


# In[125]:


# Ajustes parciais
dadosClinicosTarget = dadosClinicosTarget.astype(int);
dadosClinicosPreditoras.sex = dadosClinicos.sex.astype(bool)


# In[218]:


# 3 - Aplicando a Cross Validation (Ela faz a divisão entre dados de treino e teste, treina o modelo)
num_folds = 10
resultadoModelo1 = cross_val_score(modeloLogicR,dadosClinicosPreditoras,dadosClinicosTarget, cv = num_folds,
                                  scoring = 'accuracy')


# In[219]:


# 4 - Avaliando o modelo, usando a métrica ACURÁCIA, 
# que é o Número de previsões corretas. É útil apenas quando existe o mesmo número de 
# observações em cada classe.
print('Acurácia: %.3f' % (resultadoModelo1.mean()*100))


# #### Com padronização dos dados de treino

# In[220]:


dataX = pd.DataFrame(data = standardX)
# standardX


# In[237]:


resultadoModelo1_2 = cross_val_score(modeloLogicR,standardX,dadosClinicosArrayY, cv = num_folds,
                                  scoring = 'accuracy')


# In[238]:


print('Acurácia: %.3f' % (resultadoModelo1_2.mean()*100))
# Note que melhorou a acurácia!


# ## Aplicação de Otimização

# #### Aplicando sem a padronização dos dados

# In[239]:


# Trocando o Algoritmo por outro: Modelo Naive
modeloNaiveB = GaussianNB()
resultadoModelo2 = cross_val_score(modeloNaiveB,dadosClinicosPreditoras,dadosClinicosTarget,cv = num_folds,
                                  scoring = 'accuracy')


# In[240]:


print('Acurácia: %.3f' % (resultadoModelo2.mean()*100))


# #### Aplicando com a padronização dos dados

# In[241]:


resultadoModelo2_1 = cross_val_score(modeloNaiveB,standardX,dadosClinicosArrayY,cv = num_folds,
                                  scoring = 'accuracy')


# In[247]:


print('Acurácia: %.3f' % (resultadoModelo2_1.mean()*100))


# #### Aplicando sem a padronização dos dados

# In[248]:


# Modelo: SVM
modeloSVM = SVC()
resultadoModelo3 = cross_val_score(modeloSVM,dadosClinicosPreditoras,dadosClinicosTarget,cv = num_folds,
                                  scoring = 'accuracy')


# In[249]:


print('Acurácia: %.3f' % (resultadoModelo3.mean()*100))


# #### Aplicando com a padronização dos dados

# In[250]:


# Modelo: SVM
modeloSVM = SVC()
resultadoModelo3_1 = cross_val_score(modeloSVM,standardX,dadosClinicosArrayY,cv = num_folds,
                                  scoring = 'accuracy')


# In[251]:


print('Acurácia: %.3f' % (resultadoModelo3_1.mean()*100))


# In[252]:


# O que obteve melhor desempenho foi algoritmo Naive e Logitic, com os dados padronizados


# #### Feature Selection. Seleção das melhores variáveis para treinar o modelo. Usaremos a técnica de Eliminação Recursiva de Atributos (RFE), que permite conhecer os atributos que mais contribuem para prever o target. 

# In[253]:


# Técnica RFE
rfe = RFE(modeloLogicR, 4)
# Note que estamos com variáveis padronizadas aqui (treino)
fit = rfe.fit(dadosClinicosArrayX,dadosClinicosArrayY)


# In[254]:


# Imprimindo quais são essas variáveis
print("Variáveis Preditoras:", dadosClinicosPreditoras.columns[0:12])
print("Variáveis Selecionadas: %s" % fit.support_)
print("Ranking dos Atributos: %s" % fit.ranking_)
print("Número de Melhores Atributos: %d" % fit.n_features_)

# Note que foi anaemia, ejection_fraction, high_blood_pressure, serum_creatinine, gerando um novo
# modelo com somente elas. 


# In[264]:


dadosClinicosPreditorasOtimizado = standardX #dadospadronizados aqui
#dadosClinicosPreditorasOtimizado = dadosClinicosPreditorasOtimizado.drop(columns = ['age','creatinine_phosphokinase','diabetes',
#                                                                                    'platelets','serum_sodium','sex','smoking','time'])


# In[265]:


# Remoção de colunas, somente deixando as variáveis importantes
dadosClinicosPreditorasOtimizado = np.delete(dadosClinicosPreditorasOtimizado,[0,2,3,6,8,9,10,11],axis = 1)


# In[269]:


resultadoModelo4 = cross_val_score(modeloLogicR,dadosClinicosPreditorasOtimizado,dadosClinicosArrayY, cv = num_folds,
                                  scoring = 'accuracy')
# dadosClinicosArrayX,dadosClinicosArrayY


# In[268]:


print('Acurácia: %.3f' % (resultadoModelo4.mean()*100))


# In[270]:


resultadoModelo5 = cross_val_score(modeloNaiveB,dadosClinicosPreditorasOtimizado,dadosClinicosArrayY, cv = num_folds,
                                  scoring = 'accuracy')
# dadosClinicosArrayX,dadosClinicosArrayY


# In[271]:


print('Acurácia: %.3f' % (resultadoModelo5.mean()*100))
# Note que a acurácia caiu, portanto usaremos todas as variáveis.

