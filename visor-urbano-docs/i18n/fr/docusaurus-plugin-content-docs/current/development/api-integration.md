# 🔗 Intégration API-Storybook-Swagger

Cette section documente l'intégration complète entre les routes frontend, les composants Storybook et les endpoints de l'API backend, offrant une expérience de développement unifiée.

## 🎯 Objectif

Créer un mappage clair et accessible qui permet aux développeurs de :

- **Naviguer rapidement** entre frontend et backend
- **Trouver des composants réutilisables** dans Storybook
- **Comprendre les endpoints d'API disponibles** dans Swagger
- **Maintenir la cohérence** dans le développement

## 📊 Liens Rapides

| Outil              | URL Locale                                          | Description                                 |
| ------------------ | --------------------------------------------------- | ------------------------------------------- |
| 🎨 **Storybook**   | [localhost:6006](http://localhost:6006)             | Documentation interactive des composants UI |
| 📡 **API Swagger** | [localhost:8000/docs](http://localhost:8000/docs)   | Documentation complète des endpoints REST   |
| 🔧 **API ReDoc**   | [localhost:8000/redoc](http://localhost:8000/redoc) | Vue alternative et élégante de l'API        |
| 📖 **Docusaurus**  | [localhost:3000](http://localhost:3000)             | Cette documentation technique               |

## 🗺️ Mappage Interactif

import ApiIntegrationTable from '@site/src/components/ApiIntegrationTable';

<ApiIntegrationTable />

## 🛠️ Comment Utiliser Cette Documentation

### Pour les Développeurs Frontend

1. **Avant de créer un nouveau composant :**

   - Recherchez dans Storybook des composants similaires existants
   - Examinez les modèles de conception établis
   - Consultez le tableau d'intégration pour des exemples d'utilisation

2. **Lors du travail sur une route :**

   - Identifiez quels endpoints vous avez besoin depuis le tableau
   - Vérifiez la documentation Swagger pour comprendre les schémas
   - Utilisez les composants Storybook existants quand c'est possible

3. **Pour maintenir la cohérence :**
   - Suivez les modèles établis dans des routes similaires
   - Utilisez les mêmes composants de base pour les éléments communs
   - Gardez la nomenclature cohérente avec le reste du projet

### Pour les Développeurs Backend

1. **Lors de la création de nouveaux endpoints :**

   - Documentez clairement dans Swagger avec des exemples
   - Utilisez une nomenclature cohérente avec des endpoints similaires
   - Groupez les endpoints liés dans le même routeur

2. **Pour l'intégration frontend :**

   - Examinez quelles routes frontend consommeront votre API
   - Assurez-vous que les schémas sont clairs et complets
   - Considérez les cas d'erreur et validez les réponses

3. **Maintenance :**
   - Mettez à jour la documentation lors du changement d'endpoints
   - Exécutez le script de génération après des changements importants

### Pour DevOps et QA

1. **Validation d'intégration :**

   - Utilisez les liens directs pour tester chaque composant
   - Vérifiez que les endpoints répondent correctement
   - Validez que la documentation est à jour

2. **Automatisation :**
   - Le script `generate-api-docs.sh` devrait s'exécuter en CI/CD
   - Les liens devraient être validés automatiquement
   - La documentation devrait se régénérer à chaque déploiement

## 🔄 Automatisation

### Régénérer la Documentation

```bash
# Méthode 1 : Script direct
./scripts/generate-api-docs.sh

# Méthode 2 : Commande npm/pnpm
pnpm docs:generate-api

# Méthode 3 : Dans le flux de développement
pnpm dev:docs  # Inclut la régénération automatique
```

### Configuration CI/CD

Pour maintenir la documentation toujours à jour, ajoutez ceci à votre pipeline :

```yaml
# .github/workflows/docs.yml
- name: Generate API Documentation
  run: |
    ./scripts/generate-api-docs.sh
    git add docs/development/generated-api-integration.md
    git commit -m "docs: update API integration mapping" || true
```

## 📋 Conventions

### Nomenclature des Stories

```typescript
// ✅ Correct
export default {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
};

// ❌ À éviter
export default {
  title: 'login-form',
  component: LoginForm,
};
```

### Documentation des Endpoints

```python
# ✅ Correct
@router.get("/business-licenses/",
    summary="List business licenses",
    description="Retrieve a paginated list of business licenses with optional filtering",
    response_model=BusinessLicenseResponse
)

# ❌ À éviter
@router.get("/licenses/")  # Sans documentation
```

## 🎨 Modèles de Conception

### Composants de Base

| Composant | Usage              | Storybook                                                                        |
| --------- | ------------------ | -------------------------------------------------------------------------------- |
| `Button`  | Toutes les actions | [Voir dans Storybook](http://localhost:6006/?path=/docs/components-button--docs) |
| `Input`   | Formulaires        | [Voir dans Storybook](http://localhost:6006/?path=/docs/components-input--docs)  |
| `Table`   | Listes de données  | [Voir dans Storybook](http://localhost:6006/?path=/docs/components-table--docs)  |
| `Modal`   | Fenêtres popup     | [Voir dans Storybook](http://localhost:6006/?path=/docs/components-modal--docs)  |

### Modèles d'API

| Modèle        | Endpoint                   | Description                  |
| ------------- | -------------------------- | ---------------------------- |
| Liste         | `GET /v1/resource/`        | Lister avec pagination       |
| Détail        | `GET /v1/resource/{id}`    | Obtenir par ID               |
| Créer         | `POST /v1/resource/`       | Créer une nouvelle ressource |
| Mettre à jour | `PUT /v1/resource/{id}`    | Mettre à jour existant       |
| Supprimer     | `DELETE /v1/resource/{id}` | Supprimer ressource          |

## 📚 Ressources Additionnelles

- [Documentation Auto-Générée](./generated-api-integration) - Mappage complet mis à jour
- [README de Développement](./README.md) - Guide pour les contributeurs
- [Architecture du Projet](../getting-started/overview) - Vue d'ensemble du système

## 🤝 Contribuer

1. **Ajouter de nouveaux composants :** Créez la story correspondante dans Storybook
2. **Nouveaux endpoints :** Documentez dans Swagger et exécutez le script de génération
3. **Nouvelles routes :** Assurez-vous de mapper les composants et APIs utilisés
4. **Améliorations :** Suggérez des améliorations à cette documentation ou au script d'automatisation

---

> 💡 **Astuce :** Cette documentation est un point de départ. Le mappage exact et mis à jour sera toujours dans la [documentation auto-générée](./generated-api-integration).
