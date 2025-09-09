# 📚 Documentação da API

Esta seção documenta as práticas e padrões para criação e manutenção da documentação da API do Visor Urbano.

## 🎯 Objetivo

Fornecer diretrizes para:

- Documentação consistente de endpoints
- Padrões de resposta da API
- Validação e testes de documentação
- Integração com ferramentas de documentação

## 🛠️ Ferramentas

### Swagger/OpenAPI

- **URL Local**: [localhost:8000/docs](http://localhost:8000/docs)
- **Descrição**: Interface interativa para explorar a API
- **Uso**: Teste de endpoints em tempo real

### ReDoc

- **URL Local**: [localhost:8000/redoc](http://localhost:8000/redoc)
- **Descrição**: Vista elegante da documentação
- **Uso**: Consulta rápida de referências

## 📝 Padrões de Documentação

### Estrutura de Endpoints

- Descrição clara do propósito
- Parâmetros obrigatórios e opcionais
- Exemplos de requisição e resposta
- Códigos de status possíveis

### Schemas de Dados

- Validação de tipos
- Campos obrigatórios
- Exemplos de dados
- Relacionamentos entre entidades

## 🔗 Integração

Para mais informações sobre integração entre API e frontend, consulte [Integração API](./api-integration.md).

## 🤝 Contribuindo

Ao adicionar novos endpoints:

1. Documente no código com docstrings
2. Adicione exemplos práticos
3. Teste a documentação gerada
4. Atualize este guia conforme necessário
