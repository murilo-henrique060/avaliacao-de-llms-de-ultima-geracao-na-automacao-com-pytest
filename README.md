# Avaliação de LLMs de Última Geração na Automação com Pytest

Este repositório reúne os prompts, casos de teste, resultados de execução, cálculo de métricas híbridas e gerador de visualização dos dados para o teste de geração de casos de teste com LLMs em python.

Este repositório tem como organização:

* `/prompts` - prompts utilizados para cada caso de teste, além do modelo padronizado;
* `/cases` - código com erros mapeados para verificação dos códigos gerados pelas LLMs;
* `/results` - código gerado pelas LLMs em cada teste e resultados de sua execução com Pytest em cada geração;
* `geracao-casos-de-teste-com-llm.csv` - arquivo com métricas híbridas mapeadas para cada caso;
* `gerador-graficos.ipynb` - código para geração das visualizações de dados utilizadas nos artigos. 