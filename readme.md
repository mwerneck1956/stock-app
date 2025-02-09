# Readme

## Descrição

O **Stock-App** é uma aplicação desenvolvida para analisar dados de ações de empresas como Apple (AAPL) e Google (GOOGL). O projeto utiliza dados históricos para gerar visualizações que auxiliam na compreensão do desempenho dessas ações ao longo do tempo.

## Funcionalidades

- Leitura de dados históricos das ações da Apple e do Google.
- Geração de gráficos para visualização do desempenho das ações.
- Armazenamento seguro de credenciais para acesso a serviços em nuvem.


## Estrutura do Projeto
O projeto foi estruturado com as seguintes etapas principais:

1. **Coleta de Dados**: Utilizando a biblioteca `yfinance`, os dados históricos das ações são baixados para um intervalo de tempo especificado.
2. **Processamento dos Dados**: Os dados são particionados por dia, armazenados e submetidos a verificações de qualidade.
3. **Análises Estatísticas**: Cálculo das ações que mais variaram em valor e média móvel dos preços de fechamento.
4. **Visualização**: Geração de gráficos para melhor compreensão das tendências de mercado.
5. **Armazenamento Seguro**: Envio dos dados processados para um bucket no Google Cloud.

## Decisões de Projeto
- **Uso do `prefect` para orquestração**: Permite um fluxo estruturado e monitorável das tarefas.
- **Retry com `tenacity`**: Implementado para lidar com falhas intermitentes na coleta de dados.
- **Armazenamento no Google Cloud**: Garante persistência e acessibilidade dos dados processados.
- **Uso de `matplotlib` para visualização**: Fornece gráficos intuitivos para análise de tendências.

## Dificuldades Encontradas e Soluções
### 1. Falhas na Coleta de Dados
- **Problema**: Algumas requisições para `yfinance` falhavam devido a instabilidades na API.
- **Solução**: Implementamos `retry` com `tenacity`, permitindo múltiplas tentativas antes de registrar um erro.

## Configuração de Conta de Serviço no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com).  
2. No menu de navegação, clique em **IAM e Admin** > **Contas de Serviço**.  
3. Clique em **Criar Conta de Serviço**.  
   - Forneça um nome para a conta de serviço.  
   - Adicione uma descrição (opcional).  
   - Clique em **Criar e Continuar**.  
4. Atribua as permissões necessárias:  
   - **Storage Object Viewer**: para leitura de objetos no bucket.  
   - **Storage Object Creator**: para escrita de objetos no bucket.  
   - **Storage Object Admin**: para permissões completas de leitura e escrita.  
   - Após adicionar as permissões, clique em **Concluído**.  
5. No painel de contas de serviço, clique nos três pontos à direita da conta criada e selecione **Gerenciar Chaves**.  
6. Clique em **Adicionar Chave** > **Criar Nova Chave**.  
   - Escolha o formato JSON.  
   - Baixe o arquivo gerado e salve-o na sua conta do prefect como blocks

Agora, seu ambiente está configurado para acessar o bucket do Google Cloud.

### Etapa de Configuração: Adicionando o Nome do Bucket

Certifique-se de adicionar o `bucket-name` na configuração dos blocks no prefect

## Ativando o ambiente  
```bash
make active-environment
```

## Installing the dependencies
```bash
pip install -r requirements.txt
```

### Prefect Login 

```bash
make prefect-login API_KEY={API_KEY}
```  

## Run the project

Finally, to run the project:

```bash
make run
```  


