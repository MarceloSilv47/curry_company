# 1. Problema de negócio 

A Cury Company é uma empresa de tecnologia, localizada na Índia, que criou um aplicativo de delivery de comida, similar ao Ifood, o qual conecta restaurantes, entregadores e clientes. Ou seja, através do aplicativo o cliente consegue fazer um pedido em um determinado restaurante da região e um entregador cadastrado busca o pedido e realiza a entrega.

Mas embora gere muitos dados sobre as entregas, a empresa ainda carece de evolução na área de dados, para que com os tais, os gestores possam tomar decisões mais analíticas e assertivas que possam gerar mais lucro à empresa.

Ciente da situação, o CEO da empresa que planeja que o time de dados use técnicas de machine learning futuramente, determinou que no atual momento da companhia seria fundamental descobrir quais as principais métricas de negócio (KPIs) da Cury Company, ou seja, foi definido que será realizada uma análise de dados com ilustrações gráficas das KPIs, organizadas em uma única ferramenta, detalhando as 3 frentes da empresa, os restaurantes, os entregadores e os clientes.

# 2. Premissas do negócio 

1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022. 
2. Marketplace foi o modelo de negócio assumido. 
3. As 3 principais visões do negócio foram: Visão transação de pedidos, visão restaurante e visão entregadores.


# 3. Estratégia da solução 

## O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa: 

1. Visão do crescimento da empresa.
2. Visão do crescimento dos restaurantes.
3. Visão do crescimento dos entregadores.

## Cada visão é representada pelo seguinte conjunto de métricas. 

### 1. Visão do crescimento da empresa:

1. Pedidos por dia.
2. Porcentagem de pedidos por condições de trânsito.
3. Quantidade de pedidos por tipo e por cidade.
4. Pedidos por semana.
5. Quantidade de pedidos por tipo de entrega.
6. Quantidade de pedidos por condições de trânsito e tipo de cidade.

### 2. Visão do crescimento dos restaurantes:
1. Quantidade de pedidos únicos. 
2. Distância média percorrida. 
3. Tempo médio de entrega durante festival e dias normais. 
4. Desvio padrão do tempo de entrega durante festivais e dias normais. Tempo de entrega médio por cidade. 
5. Distribuição do tempo médio de entrega por cidade.
6. Tempo médio de entrega por tipo de pedido. 

### 3. Visão do crescimento dos entregadores 
1. Idade do entregador mais velho e do mais novo. 
2. Avaliação do melhor e do pior veículo. 
3. Avaliação média por entregador. 
4. Avaliação média por condições de trânsito. 
5. Avaliação média por condições climáticas. 
6. Tempo médio do entregador mais rápido. 
7. Tempo médio do entregador mais rápido por cidade.


# 4. Top 3 Insights de dados 

1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais. 
2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito. 
3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado.

# 5. O produto final do projeto 

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através desse link: https://marcelosilv47-curry-company-home-pdrwtr.streamlit.app/


# 6. Conclusão 

O objetivo desse projeto foi criar um conjunto de gráficos e/ou tabelas que ilustrassem as principais métricas da empresa da melhor forma possível para o CEO. Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022. Pode-se concluir então, que o objetivo foi alcançado.

# 7. Próximo passos  

1. Reduzir o número de métricas.
2. Criar novos filtros. 
3. Adicionar novas visões de negócio.

