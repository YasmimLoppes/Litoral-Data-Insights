#  Litoral Data Insights — Painel de Dados Econômicos da Baixada Santista

> Transformando dados públicos em inteligência prática para pequenos negócios da região onde moro

---

##  Por que eu criei esse projeto?

Moro em São Vicente e vejo isso todo dia: donos de pequenos negócios — padarias, lojas, salões, pousadas — tomam decisões importantes sem ter as informações certas. Alguém abre uma loja pensando que ali tem público, mas não tem; investe num produto que a região não consome; escolhe um bairro sem saber quanto as pessoas ganham, quantas moram ali, ou quais setores já existem. Tudo no "achômetro".

Os dados não faltam o IBGE, o SEADE, as prefeituras e o Ministério do Trabalho têm tudo isso disponível. O problema é que estão espalhados em dezenas de sites, em formatos diferentes, com nomes de bairros escritos de formas diferentes, valores faltantes e sem nenhuma organização. Para uma pessoa que não trabalha com dados, é praticamente impossível juntar tudo e entender.

Foi aí que pensei: e se eu pegasse todos esses dados, limpasse, organizasse e apresentasse de um jeito que qualquer pessoa consiga usar? Não para fazer gráficos bonitos, mas para responder perguntas reais: "Vale a pena abrir minha loja aqui?", "Meus clientes potenciais têm qual renda?", "Qual setor tem pouca concorrência mas muita demanda?". Esse é o objetivo do projeto.

---

##  Ferramentas utilizadas

| Ferramenta | Para que serve | Por que escolhi ela |
|---|---|---|
|   Python | Extrair, limpar e transformar os dados | É a linguagem mais usada em dados, tem bibliotecas que leem, organizam e calculam tudo com facilidade |
|   SQL | Cruzar, agrupar e validar informações | Permite juntar dados de tabelas diferentes e fazer perguntas específicas de forma rápida e estruturada |
|   Power BI | Criar o painel visual com mapas e gráficos | É gratuito, muito usado no mercado e permite que qualquer pessoa filtre e veja os dados sem saber programar |
|   Fluxo ETL | Extração → Transformação → Carga → Visualização | É o padrão da indústria de dados — o caminho completo desde o dado bruto até a informação pronta para usar |

---

##  Como foi construído — passo a passo

### 1. Extração dos dados — de onde vem tudo?
Primeiro preciso buscar a informação bruta. Não inventei nenhum número — tudo vem de fontes oficiais e públicas: IBGE, SEADE, RAIS/MTE e prefeituras municipais. Cada fonte entrega os dados num formato diferente — um é CSV, outro é JSON, outro é página de site. O código lê cada um, extrai o que importa e junta tudo numa mesma estrutura unificada. É como se cada fonte falasse um idioma diferente e eu criasse um tradutor que deixa todo mundo falando a mesma língua.

### 2. Limpeza e padronização — por que essa etapa é a mais importante?
Dados públicos quase nunca vêm prontos para usar. É muito comum encontrar o mesmo lugar escrito de 3 formas diferentes, células vazias, números com separadores inconsistentes e informações duplicadas. Nessa etapa eu corrijo tudo: padronizo nomes, trato valores faltantes sem inventar informação, removo duplicatas e confiro se os números fazem sentido. Se eu pular essa etapa, todo o resto vai estar errado — "lixo entra, lixo sai", como se diz na área de dados. Por isso essa é a parte que mais toma tempo e mais atenção.

### 3. Cruzamento e análise — o que os dados dizem quando estão juntos?
Aqui é onde a informação ganha sentido. Separadamente, saber a renda de uma cidade ou quantas lojas existem não diz muita coisa. Mas quando eu cruzo essas informações — renda média × quantidade de empresas × população — eu descubro coisas que ninguém vê olhando os dados separados: quais bairros têm renda acima da média mas pouca oferta de comércio, quais cidades têm população crescente mas poucos serviços, onde existe demanda potencial que ainda não foi atendida. Sem cruzar os dados, esses padrões ficam escondidos. Com o cruzamento, aparecem claramente.

### 4. Visualização — transformar números em entendimento
De que adianta ter dados limpos e cruzados se só quem sabe programar consegue ler? A última etapa é construir um painel no Power BI onde qualquer pessoa — mesmo quem nunca trabalhou com dados — consegue clicar numa cidade, ver renda, população e principais setores, filtrar por tipo de negócio e comparar entre cidades. O objetivo final não é o dado em si — é a decisão que alguém toma por causa dele.

---

##   O que esse projeto entrega

-   Visão consolidada de renda e população por cidade da Baixada Santista
-   Distribuição de empresas por setor econômico onde tem mais e onde tem menos
-   Identificação de regiões com potencial de crescimento ou demanda não atendida
-   Dados organizados e prontos para usar em tomada de decisão sem precisar procurar em 10 sites diferentes
-   Base pronta para ser atualizada com novos dados conforme forem publicados

---

## Por que esse projeto é diferente?

Projetos de curso geralmente usam dados já limpos, organizados e prontos você só precisa rodar o código e ver o gráfico aparecer. Na vida real não é assim: os dados vêm bagunçados, incompletos e espalhados. Esse projeto reflete exatamente a realidade do dia a dia de quem trabalha com dados: os dados são reais e públicos, não inventados; o tratamento é necessário e não opcional; e o resultado final tem um propósito claro ajudar pessoas da minha região a tomarem decisões melhores.

---

**Feito por Yasmim Loppes** | São Vicente/SP
