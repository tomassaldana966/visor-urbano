# 👨‍💻 Guide de Développement

Bienvenue dans la documentation de développement de Visor Urbano. Cette section contient des guides complets pour les développeurs contribuant au projet.

## 🚀 Démarrage Rapide

Si vous êtes nouveau sur le projet, commencez ici :

1. **Configuration Système** - Prérequis et installation
2. **Configuration Rapide** - Démarrer rapidement
3. **[Intégration API](./api-integration.md)** - Comprendre l'intégration complète de la pile

## 📚 Documentation de Développement

### Développement Principal

- **[Intégration API](./api-integration.md)** - Mappage Route-Composant-Endpoint

### Architecture

Notre développement suit une architecture full-stack moderne :

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI + SQLAlchemy
- **Base de données**: PostgreSQL avec PostGIS pour les données géospatiales
- **Documentation**: Storybook + Swagger + Docusaurus
- **Tests**: Vitest + Playwright + Pytest

## 🛠️ Outils de Développement

| Outil            | Objectif                       | URL                           |
| ---------------- | ------------------------------ | ----------------------------- |
| **Storybook**    | Développement de Composants UI | `http://localhost:6006`       |
| **Swagger UI**   | Documentation API              | `http://localhost:8000/docs`  |
| **ReDoc**        | Vue Alternative de l'API       | `http://localhost:8000/redoc` |
| **Docusaurus**   | Documentation Technique        | `http://localhost:3000`       |
| **Frontend Dev** | Application React              | `http://localhost:5173`       |

## 🏗️ Structure du Projet

```
visor-urbano/
├── apps/
│   ├── frontend/        # Application React TypeScript
│   ├── backend/         # Serveur Python FastAPI
│   └── e2e/            # Tests de bout en bout
├── packages/
│   ├── ui/             # Composants UI partagés
│   └── eslint-config/  # Configuration ESLint partagée
├── docs/               # Documentation du projet
└── scripts/            # Scripts d'automatisation
```

## 🔄 Flux de Développement

### 1. Configuration de l'Environnement Local

```bash
# Cloner le dépôt
git clone <repository-url>
cd visor-urbano

# Installer les dépendances
pnpm install

# Configurer la base de données
cd apps/backend
docker-compose up -d

# Démarrer les services de développement
pnpm dev
```

### 2. Développement Frontend

```bash
# Démarrer le serveur de développement
cd apps/frontend
pnpm dev

# Démarrer Storybook
pnpm storybook

# Exécuter les tests
pnpm test
```

### 3. Développement Backend

```bash
# Démarrer le serveur API
cd apps/backend
pnpm dev

# Exécuter les migrations
pnpm migrate

# Exécuter les tests
pnpm test
```

## 📝 Conventions de Code

### Frontend

- **Framework**: React 18+ avec TypeScript strict
- **Styling**: Tailwind CSS avec des composants shadcn/ui
- **État**: Zustand pour la gestion d'état global
- **Routage**: React Router v6
- **Formulaires**: React Hook Form avec validation Zod

### Backend

- **Framework**: FastAPI avec SQLAlchemy ORM
- **Base de données**: PostgreSQL avec PostGIS
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Tests**: Pytest avec couverture

### Style de Code

- **Formatage**: Prettier pour frontend, Black pour backend
- **Linting**: ESLint pour frontend, Ruff pour backend
- **Commits**: Conventional commits avec liens vers les issues

## 🧪 Tests et Qualité

### Types de Tests

1. **Tests Unitaires**: Vitest (frontend) + Pytest (backend)
2. **Tests d'Intégration**: API et base de données
3. **Tests E2E**: Playwright pour les flux utilisateur
4. **Tests de Composants**: Storybook + Testing Library

### Couverture de Code

- **Objectif**: >90% de couverture pour les nouvelles fonctionnalités
- **Outils**: Vitest Coverage + Coverage.py
- **Rapports**: Intégrés dans CI/CD

## 🚦 Pipeline CI/CD

### Branches et Stratégie

- **main**: Code de production stable
- **develop**: Code de développement intégré
- **feature/\***: Nouvelles fonctionnalités
- **hotfix/\***: Corrections urgentes

### Contrôles Automatisés

1. **Linting et formatage**
2. **Tests unitaires et d'intégration**
3. **Contrôles de sécurité**
4. **Analyse de la couverture de code**
5. **Construction et déploiement**

## 🤝 Contribution

### Processus de Contribution

1. **Fork** le dépôt
2. **Créer** une branche feature
3. **Développer** avec des tests
4. **Tester** localement
5. **Soumettre** une pull request

### Checklist de Pull Request

- [ ] Tests passent localement
- [ ] Code formaté et linté
- [ ] Documentation mise à jour
- [ ] Changements décrits clairement
- [ ] Review demandée aux mainteneurs

## 📖 Ressources Supplémentaires

- **[Guide API](./api-integration.md)** - Intégration complète frontend-backend

---

**💡 Conseil**: Gardez cette documentation à jour au fur et à mesure que le projet évolue. La documentation obsolète est pire qu'aucune documentation !
