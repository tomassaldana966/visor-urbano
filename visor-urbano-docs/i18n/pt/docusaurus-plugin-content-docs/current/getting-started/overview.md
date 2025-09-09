---
sidebar_position: 1
title: Visão Geral
description: Introdução ao sistema de gestão municipal Visor Urbano
---

# Visor Urbano - Visão Geral

Visor Urbano é uma plataforma moderna de gestão urbana e planejamento municipal projetada para ser implementada e adaptada por cidades ao redor do mundo.

## 🎯 O que é o Visor Urbano?

**Visor Urbano** é um sistema abrangente que permite às prefeituras:

- 📋 **Gerenciar procedimentos** digitalmente (licenças, permissões, certificados)
- 🗺️ **Visualizar informações geoespaciais** com mapas interativos
- 🏘️ **Gerenciar zoneamento urbano** e regulamentações
- 👥 **Gerenciar usuários** com diferentes funções e permissões
- 📊 **Gerar relatórios** e análises de dados
- 🔄 **Automatizar processos** administrativos

## 🚀 Stack Tecnológico

### Frontend

- **React 19** + TypeScript
- **Vite** para desenvolvimento rápido
- **OpenLayers** para mapas interativos
- **Tailwind CSS** para estilização
- **react-i18next** para internacionalização

### Backend

- **FastAPI** + Python 3.13
- **PostgreSQL** + PostGIS para dados geoespaciais
- **SQLAlchemy** + Alembic para ORM e migrações
- **JWT** com authlib para autenticação segura

### Infraestrutura

- **Docker** + Docker Compose
- **Turborepo** para monorepo
- **pnpm** para gestão de dependências

## 🌍 Casos de Uso por País

### 🇨🇱 Chile - Piloto Nova Versão

- Licenças de construção segundo OGUC
- Patentes comerciais
- Certificados de informações prévias
- Integração com SII e Registro Civil

### 🇲🇽 México - Versão Clássica

- Licenças municipais
- Licenças comerciais
- Certificados de desenvolvimento urbano

## 🛠️ Início Rápido

1. **Requisitos do Sistema**: Docker, Node.js 18+, Python 3.13
2. **Instalação**: Clonar repositório e executar configuração
3. **Configuração**: Adaptar para seu município
4. **Implantação**: Configuração Docker pronta para produção

## 📖 Estrutura da Documentação

Esta documentação está organizada em:

- **Primeiros Passos**: Instalação e configuração
- **Adaptação Urbana**: Implementações específicas por país
- **Desenvolvimento**: Documentação da API e componentes
- **Implantação**: Guias de produção

## 🤝 Comunidade Global

Visor Urbano é projetado para replicação internacional com:

- Suporte multi-idioma (Espanhol, Inglês, Francês, Português)
- Estruturas legais adaptáveis
- Guias de implementação regionais
- Comunidade de desenvolvimento ativa

---

Pronto para começar? Confira nosso [guia de configuração rápida](./quick-setup) ou navegue pelas implementações específicas para sua região.
