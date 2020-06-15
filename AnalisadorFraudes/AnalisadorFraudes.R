# Descrição
# Objetivo: Prever se o usuário fará o download de um aplicativo ou não
# após clicar em um anúncio. Em suma, prever a ocorrência de fraudes
# (cliques que não confirmam em download de aplicativos)

# 1 - Definindo o diretório do local de trabalho
setwd("C:/FCD/BigDataRAzure/AnalisadorFraudes")
getwd()

# Pacotes
library(lubridate)
library(caTools)
library(rpart)
library(e1071)

# 2 - Carregando o dataset
# Opção pelo dataset de amostra devido aos recursos limitados do computador (armazenamento de memória)
# principal e dataset muito grande
registros <- read.csv("datasets/train_sample.csv")
nrow(registros)

# 3 - Análise Exploratória
View(registros)

# Resumo sobre cada tipo de dados, dimensões
str(registros)

# 4 - Pré-processamento, limpeza, transformação e preparação
# Transformação de variáveis numéricas para categóricas ou vice-versa, segundo
# informações colhidas do dicionário de dados
registros$ip = as.factor(registros$ip)
registros$app = as.factor(registros$app)
registros$device = as.factor(registros$device)
registros$os = as.factor(registros$os)
registros$channel = as.factor(registros$channel)
registros$is_attributed = as.factor(registros$is_attributed)

# Conversão para data
registros$click_time = ymd_hms(registros$click_time) 
registros$attributed_time = ymd_hms(registros$attributed_time) 


# Exploração de variáveis categóricas
table(registros$ip)
range(as.integer(table(registros$ip)))
top5IPsMaisFrequentes = head(sort((table(registros$ip)),decreasing = TRUE), 5L)
View(top5IPsMaisFrequentes)
png("Img1.png", width = 500, height = 500, res = 72)
barplot(top5IPsMaisFrequentes,main = "TOP 5 (Quantidade) IDS dos Usuários",
        xlab = "ID do Usuário",ylab = "Quantidade",col = "yellow")
# hist(as.integer(registros$ip),main = "Frequência(Quantidade) Endereços IP",
# xlab = "Valores IP", ylab = "Frequência", col = "yellow")
dev.off()

# A maior frequência IP é 0 .. 3000


table(registros$app)
range(as.integer(table(registros$app)))
#hist(as.integer(registros$app),main = "Frequência(Quantidade) IDs do APP na Loja",
#     xlab = "ID do App", ylab = "Quantidade", col = "yellow")
# Insight - ID mas usado: 0 ..15
# TOP 5 categorias mais frequentes
top5AppsMaisFrequentes = head(sort((table(registros$app)),decreasing = TRUE), 5L)
View(top5AppsMaisFrequentes)

#barplot(table(registros$app),main = "(Quantidade) IDS dos APPs",
#        xlab = "ID do Dispositivo",ylab = "Quantidade",col = "yellow")
# Insight - ID mas usado: 3
png("Img2.png", width = 500, height = 500, res = 72)
barplot(top5AppsMaisFrequentes,main = "TOP 5 - (Quantidade) IDS dos APPs",
        xlab = "ID do Dispositivo",ylab = "Quantidade",col = "yellow")
dev.off()


table(registros$device)
range(as.integer(table(registros$device)))
top5DispositivosMaisFrequentes = head(sort((table(registros$device)),decreasing = TRUE), 5L)
View(top5DispositivosMaisFrequentes)
barplot(table(registros$device),main = "Dispositivos usados",
        xlab = "Código do tipo de dispositivo",ylab = "Quantidade",col = "yellow")
png("Img3.png", width = 500, height = 500, res = 72)
barplot(top5DispositivosMaisFrequentes,main = "TOP 5 - Dispositivos usados",
        xlab = "Código do tipo de dispositivo",ylab = "Quantidade",col = "yellow")
dev.off()
hist(as.integer(registros$device),main = "Frequência(Quantidade) Dispositivos usados",
     xlab = "ID do Dispositivo", ylab = "Quantidade", col = "yellow")
# Insight 2 - Dispositivos de cÃ³digo 1 e 4 foram os mais usados

table(registros$os)
count.fields()
range(as.integer(registros$os))
top5SistemasMaisFrequentes = head(sort((table(registros$os)),decreasing = TRUE), 5L)
View(top5SistemasMaisFrequentes)
#barplot(table(registros$os),main = "Sistemas Operacionais usados",
#        xlab = "Código do tipo de sistema operacional",ylab = "Quantidade", col = "yellow")
png("Img4.png", width = 500, height = 500, res = 72)
barplot(top5SistemasMaisFrequentes,main = "TOP 5 - Sistemas Operacionais usados",
        xlab = "Código do tipo de sistema operacional",ylab = "Quantidade", col = "yellow")
dev.off()
hist(as.integer(registros$os),main = "Frequência(Quantidade) Sistemas usados",
     xlab = "ID do Sistema", ylab = "Quantidade", col = "yellow")
# Insight 3 - OS de Códigos entre 13 e 18 foram os mais usados
# 10 - 20 os mais frequentes

table(registros$channel)
range(as.integer(table(registros$channel))) # Menor e maior categoria
top5CanaisMaisFrequentes = head(sort((table(registros$channel)),decreasing = TRUE), 5L)
View(top5CanaisMaisFrequentes)
#barplot(table(registros$channel),main = "Canais usados",
#        xlab = "Código do tipo do canal",ylab = "Quantidade", col = "yellow")
png("Img5.png", width = 500, height = 500, res = 72)
barplot(top5CanaisMaisFrequentes,main = "TOP 5 - Canais usados",
        xlab = "Código do tipo do canal",ylab = "Quantidade", col = "yellow")
#hist(as.integer(registros$channel),main = "Frequência(Quantidade) dos Canais Usados",
#     xlab = "ID do Canal", ylab = "Quantidade", col = "yellow")
# Insight 4 - Os canais variam bastante, sendo o mais comum entre 300- 315
dev.off()

table(registros$is_attributed)
#barplot(table(registros$is_attributed),main = "Resultado DOWNLOAD vs NÃO DOWNLOAD",
#        xlab = "NÃO FEZ DOWNLOAD (0) FEZ DOWNLOAD (1)",ylab = "Quantidade",col = "yellow")

model_table <- table(registros$is_attributed)
model_table <- prop.table(model_table) * 100
paste(round(model_table, digits = 1),"%")


rotulos = c('NÃO FEZ DOWNLOAD (0) ','FEZ DOWNLOAD (1)')
percent = round(model_table/sum(model_table)*100,digits = 1)
rotulos = paste(rotulos,percent) # SES 40%
rotulos = paste(rotulos,"%",sep = "") # SES 40%
png("Img6.png", width = 500, height = 500, res = 72)
pie(model_table,labels = rotulos, col = c("blue","pink"),main = "Resultado DOWNLOAD vs NÃO DOWNLOAD",
    radius = 1)
dev.off()
str(registros$click_time)
table(wday(registros$click_time,label = TRUE)) 
png("Img7.png", width = 500, height = 500, res = 72)
barplot(table(wday(registros$click_time,label = TRUE)) ,main = "Dia (da semana) do click",
        xlab = "Dia da semana",ylab = "Quantidade", col = c("gray","red",
                                                            "darkgreen","green",
                                                            "gold","blue","pink"))
dev.off()

table(month(registros$click_time,label = TRUE)) 
png("Img8.png", width = 500, height = 500, res = 72)
barplot(table(month(registros$click_time,label = TRUE)) ,main = "Mês do click",
        xlab = "MêS",ylab = "Quantidade")
dev.off()

table(hour(registros$click_time)) 
png("Img9.png", width = 500, height = 500, res = 72)
barplot(table(hour(registros$click_time)) ,main = "Hora do click",
        xlab = "MêS",ylab = "Quantidade", col = "gold")
dev.off()
png("Img10.png", width = 500, height = 500, res = 72)
hist(x = hour(registros$click_time),breaks = 24, main = "Frequência da Hora do click",
     xlab = "Hora", ylab = "Frequência", col = "gold")
dev.off()


summary(hour(registros$click_time))
png("Img11.png", width = 500, height = 500, res = 72)
boxplot(x = hour(registros$click_time),main = "Hora do click",
        ylab = "Hora", col = "gold")
dev.off()
table(mday(registros$click_time))
png("Img12.png", width = 500, height = 500, res = 72)
barplot(table(mday(registros$click_time)) ,main = "Dia do mês do click",ylab = "Quantidade",
        xlab = "Dia do MêS",breaks = 31)
dev.off()

table(hour(registros$attributed_time)) 
table(minute(registros$attributed_time)) 


# Treinamento
# 5 - Algoritmo de Machine Learni (treinamento,teste)
amostra <- sample.split(registros$is_attributed, SplitRatio = 0.70)
dados_treino = subset(registros, amostra == TRUE)
dados_teste = subset(registros, amostra == FALSE)


modelo_rf_v1 = rpart(is_attributed ~ ., data = dados_treino, control = rpart.control(cp = .0005)) #0.9974333 

# Teste (para as previsões)
# Previsões nos dados de teste
tree_pred = predict(modelo_rf_v1, dados_teste, type='class')

# Percentual de previsões corretas com dataset de teste
mediaModeloR = mean(tree_pred == dados_teste$is_attributed)  
paste(round(mean(tree_pred==dados_teste$is_attributed) * 100, digits = 1),"%")

# 7 - Otimização do modelo

# Tentativa 1 = Alterar algoritmo de ML (naiveBayes)

# Treine o modelo
?naiveBayes
modeloNaive = naiveBayes(formula = dados_treino$is_attributed ~., data = dados_treino)
# Fazendo previsões com os dados de teste
previsoes = predict(modeloNaive,dados_teste[,-1])
previsoes

# Fazendo comparações entre o original e as previsões, quantos acertos e quantos errou
resultados = cbind(previsoes,dados_teste$is_attributed)
colnames(resultados) <- c('Previsto','Real')
resultados <- as.data.frame(resultados)

# Cálculo do Erro médio
mse <- mean((resultados$Real - resultados$Previsto)^2)
print(mse)*100

# RMSE
rmse <- mse^0.5
rmse

# Confusion matrix
table(pred = previsoes, true = dados_teste$is_attributed)

# Média
mediaModeloNaive = mean(previsoes == dados_teste$is_attributed) #0.9876 98.8 %3 O algoritmo 1 teve melhor desempenho 
paste(round(mean(previsoes == dados_teste$is_attributed) * 100, digits = 1),"%")


# svm não possível pelo tamanho 9,1 G


# Tentativa 2 = Alterar variáveis preditoras do modelo
# Retirando variáveis para verificar se melhora ou modelo? Técnica subjetiva!

# Retreinando o modelo tirando 1 variável (ip)
dados_treino$ip = NULL
dados_teste$ip = NULL
modelo_rf_v2 = rpart(is_attributed ~ . , 
                     data = dados_treino, 
                     control = rpart.control(cp = .0005))


# Teste (para as previsões)
# Previsões nos dados de teste
tree_pred = predict(modelo_rf_v2, dados_teste, type='class')

# Percentual de previsões corretas com dataset de teste
mediaModeloR2 = mean(tree_pred == dados_teste$is_attributed)  
paste(round(mean(tree_pred==dados_teste$is_attributed) * 100, digits = 1),"%")


# Tentativa 3 = Alteração parâmetros do ML
# Alteração do cp da árvore (0-1 0 mais complexo, 1 menos complexo)
# Ajuste para encontrar o CP ótimo
#printcp(modelo_rf_v1) # note que a menor taxa relativa de erros com cp 0.000500, tendo 6 divisões na árvore
#plotcp(modelo_rf_v1)
#modelo_rf_v2 = rpart(is_attributed ~ ., data = dados_treino, control = rpart.control(cp = 0.0022))

#tree_pred2 = predict(modelo_rf_v2, dados_teste, type='class')
#mean(tree_pred2 == dados_teste$is_attributed) #0.9974333
#paste(round(mean(tree_pred2==dados_teste$is_attributed) * 100, digits = 1),"%")



# comparação dos modelos e qual teve melhor desempenho (precisão)
resultadosFinais <- data.frame(nome = c("Modelo 1", "Modelo 2"),
                               algoritmo = c("R-part", "naiveBayes"),
                               precisao = c(mediaModeloR2,mediaModeloNaive))
# modelo escolhido foi o modelo_rf_v2

# 9 - Resultado final (publicação do trabalho, modelo)