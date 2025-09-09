# 🔗 Integração API-Storybook-Swagger

Esta seção documenta a integração completa entre rotas frontend, componentes Storybook e endpoints da API backend, fornecendo uma experiência de desenvolvimento unificada.

## 🎯 Objetivo

Criar um mapeamento claro e acessível que permite aos desenvolvedores:

- **Navegar rapidamente** entre frontend e backend
- **Encontrar componentes reutilizáveis** no Storybook
- **Entender endpoints de API disponíveis** no Swagger
- **Manter consistência** no desenvolvimento

## 📊 Links Rápidos

| Ferramenta         | URL Local                                           | Descrição                                 |
| ------------------ | --------------------------------------------------- | ----------------------------------------- |
| 🎨 **Storybook**   | [localhost:6006](http://localhost:6006)             | Documentação interativa de componentes UI |
| 📡 **API Swagger** | [localhost:8000/docs](http://localhost:8000/docs)   | Documentação completa de endpoints REST   |
| 🔧 **API ReDoc**   | [localhost:8000/redoc](http://localhost:8000/redoc) | Vista alternativa e elegante da API       |
| 📖 **Docusaurus**  | [localhost:3000](http://localhost:3000)             | Esta documentação técnica                 |

## 🗺️ Mapeamento Interativo

import ApiIntegrationTable from '@site/src/components/ApiIntegrationTable';

<ApiIntegrationTable />

## 🛠️ Como Usar Esta Documentação

### Para Desenvolvedores Frontend

1. **Antes de criar um novo componente:**

   - Procure no Storybook por componentes similares existentes
   - Revise os padrões de design estabelecidos
   - Consulte a tabela de integração para exemplos de uso

2. **Ao trabalhar em uma rota:**

   - Identifique quais endpoints você precisa da tabela
   - Verifique a documentação do Swagger para entender os schemas
   - Use componentes existentes do Storybook quando possível

3. **Para manter consistência:**
   - Siga padrões estabelecidos em rotas similares
   - Use os mesmos componentes base para elementos comuns
   - Mantenha nomenclatura consistente com o resto do projeto

### Para Desenvolvedores Backend

1. **Ao criar novos endpoints:**

   - Documente claramente no Swagger com exemplos
   - Use nomenclatura consistente com endpoints similares
   - Agrupe endpoints relacionados no mesmo roteador

2. **Para integração frontend:**

   - Revise quais rotas frontend consumirão sua API
   - Certifique-se de que os schemas estão claros e completos
   - Considere casos de erro e valide as respostas

3. **Manutenção:**
   - Atualize a documentação ao alterar endpoints
   - Execute o script de geração após mudanças importantes

### Para DevOps e QA

1. **Validação de integração:**

   - Use links diretos para testar cada componente
   - Verifique se endpoints respondem corretamente
   - Valide se a documentação está atualizada

2. **Automação:**
   - O script `generate-api-docs.sh` deve executar no CI/CD
   - Links devem ser validados automaticamente
   - Documentação deve regenerar a cada deployment

## 🔄 Automação

### Regenerar Documentação

```bash
# Método 1: Script direto
./scripts/generate-api-docs.sh

# Método 2: Comando npm/pnpm
pnpm docs:generate-api

# Método 3: Como parte do fluxo de desenvolvimento
pnpm dev:docs  # Inclui regeneração automática
```

### Configuração CI/CD

Para manter a documentação sempre atualizada, adicione isto ao seu pipeline:

```yaml
# .github/workflows/docs.yml
- name: Generate API Documentation
  run: |
    ./scripts/generate-api-docs.sh
    git add docs/development/generated-api-integration.md
    git commit -m "docs: update API integration mapping" || true
```

## 📋 Convenções

### Nomenclatura de Stories

```typescript
// ✅ Correto
export default {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
};

// ❌ Evitar
export default {
  title: 'login-form',
  component: LoginForm,
};
```

### Documentação de Endpoints

```python
# ✅ Correto
@router.get("/business-licenses/",
    summary="List business licenses",
    description="Retrieve a paginated list of business licenses with optional filtering",
    response_model=BusinessLicenseResponse
)

# ❌ Evitar
@router.get("/licenses/")  # Sem documentação
```

## 🎨 Padrões de Design

### Componentes Base

| Componente | Uso                | Storybook                                                                     |
| ---------- | ------------------ | ----------------------------------------------------------------------------- |
| `Button`   | Todas as ações     | [Ver no Storybook](http://localhost:6006/?path=/docs/components-button--docs) |
| `Input`    | Formulários        | [Ver no Storybook](http://localhost:6006/?path=/docs/components-input--docs)  |
| `Table`    | Listagens de dados | [Ver no Storybook](http://localhost:6006/?path=/docs/components-table--docs)  |
| `Modal`    | Janelas popup      | [Ver no Storybook](http://localhost:6006/?path=/docs/components-modal--docs)  |

### Padrões de API

| Padrão    | Endpoint                   | Descrição            |
| --------- | -------------------------- | -------------------- |
| Listar    | `GET /v1/resource/`        | Listar com paginação |
| Detalhe   | `GET /v1/resource/{id}`    | Obter por ID         |
| Criar     | `POST /v1/resource/`       | Criar novo recurso   |
| Atualizar | `PUT /v1/resource/{id}`    | Atualizar existente  |
| Deletar   | `DELETE /v1/resource/{id}` | Deletar recurso      |

## 📚 Recursos Adicionais

- [Documentação Auto-Gerada](./generated-api-integration) - Mapeamento completo atualizado
- [README de Desenvolvimento](./README.md) - Guia para contribuidores
- [Arquitetura do Projeto](../getting-started/overview) - Visão geral do sistema

## 🤝 Contribuindo

1. **Adicionar novos componentes:** Crie a story correspondente no Storybook
2. **Novos endpoints:** Documente no Swagger e execute o script de geração
3. **Novas rotas:** Certifique-se de mapear componentes e APIs utilizados
4. **Melhorias:** Sugira melhorias para esta documentação ou script de automação

---

> 💡 **Dica:** Esta documentação é um ponto de partida. O mapeamento exato e atualizado estará sempre na [documentação auto-gerada](./generated-api-integration).
