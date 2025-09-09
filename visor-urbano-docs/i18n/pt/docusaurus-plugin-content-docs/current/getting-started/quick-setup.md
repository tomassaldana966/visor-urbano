# ⚡ Configuração Rápida

Esta seção fornece um guia rápido para configurar o ambiente de desenvolvimento do Visor Urbano.

## 🎯 Objetivo

Configurar rapidamente:

- Ambiente de desenvolvimento local
- Dependências necessárias
- Configurações básicas
- Primeiros testes

## 🔧 Pré-requisitos

### Software Necessário

- Node.js (versão 18 ou superior)
- Python 3.8+
- Git
- Docker (opcional, mas recomendado)

### Ferramentas de Desenvolvimento

- Editor de código (VS Code recomendado)
- Terminal/linha de comando
- Navegador web moderno

## 🚀 Instalação Rápida

### 1. Clonar o Repositório

```bash
git clone [URL_DO_REPOSITORIO]
cd visor-urbano
```

### 2. Configurar Backend

```bash
cd apps/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Configurar Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

### 4. Configurar Documentação

```bash
cd visor-urbano-docs
npm install
npm start
```

## 🌐 URLs de Desenvolvimento

### Serviços Locais

| Serviço            | URL                                               | Descrição           |
| ------------------ | ------------------------------------------------- | ------------------- |
| 🎨 **Frontend**    | [localhost:3000](http://localhost:3000)           | Interface principal |
| 📡 **API Backend** | [localhost:8000](http://localhost:8000)           | API REST            |
| 📚 **Swagger**     | [localhost:8000/docs](http://localhost:8000/docs) | Documentação da API |
| 🎭 **Storybook**   | [localhost:6006](http://localhost:6006)           | Componentes UI      |
| 📖 **Docusaurus**  | [localhost:3001](http://localhost:3001)           | Esta documentação   |

## ✅ Verificação da Instalação

### Teste Frontend

- Acesse [localhost:3000](http://localhost:3000)
- Verifique se a interface carrega corretamente
- Teste navegação básica

### Teste Backend

- Acesse [localhost:8000/docs](http://localhost:8000/docs)
- Teste alguns endpoints básicos
- Verifique conexão com banco de dados

### Teste Integração

- Verifique se frontend conecta com backend
- Teste fluxos básicos da aplicação
- Confirme funcionamento de APIs

## 🔗 Próximos Passos

### Desenvolvimento

- [Requisitos do Sistema](./system-requirements.md) - Especificações detalhadas
- [Integração API](../development/api-integration.md) - Documentação técnica
- [Visão Geral](./overview.md) - Arquitetura do sistema

### Produção

- [Implantação](../deployment/production-deployment.md) - Guia de produção

## 🛠️ Solução de Problemas

### Problemas Comuns

- **Porta em uso**: Mude as portas nos arquivos de configuração
- **Dependências**: Execute `npm install` ou `pip install -r requirements.txt`
- **Permissões**: Verifique permissões de arquivos e diretórios

### Logs e Debug

- Frontend: Console do navegador
- Backend: Logs do terminal
- Documentação: Console do npm

## 🤝 Suporte

Em caso de problemas:

1. Consulte [Requisitos do Sistema](./system-requirements.md)
2. Verifique logs de erro
3. Consulte documentação técnica
4. Contate equipe de desenvolvimento
