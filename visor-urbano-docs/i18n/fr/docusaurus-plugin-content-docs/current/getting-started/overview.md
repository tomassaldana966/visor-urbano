---
sidebar_position: 1
title: Aperçu
description: Introduction au système de gestion municipale Visor Urbano
---

# Visor Urbano - Aperçu

Visor Urbano est une plateforme moderne de gestion urbaine et de planification municipale conçue pour être mise en œuvre et adaptée par les villes du monde entier.

## 🎯 Qu'est-ce que Visor Urbano ?

**Visor Urbano** est un système complet qui permet aux municipalités de :

- 📋 **Gérer les procédures** numériquement (licences, permis, certificats)
- 🗺️ **Visualiser l'information géospatiale** avec des cartes interactives
- 🏘️ **Gérer le zonage urbain** et les réglementations
- 👥 **Gérer les utilisateurs** avec différents rôles et permissions
- 📊 **Générer des rapports** et analyses de données
- 🔄 **Automatiser les processus** administratifs

## 🚀 Stack Technologique

### Frontend

- **React 19** + TypeScript
- **Vite** pour un développement rapide
- **OpenLayers** pour les cartes interactives
- **Tailwind CSS** pour le style
- **react-i18next** pour l'internationalisation

### Backend

- **FastAPI** + Python 3.13
- **PostgreSQL** + PostGIS pour les données géospatiales
- **SQLAlchemy** + Alembic pour ORM et migrations
- **JWT** avec authlib pour l'authentification sécurisée

### Infrastructure

- **Docker** + Docker Compose
- **Turborepo** pour monorepo
- **pnpm** pour la gestion des dépendances

## 🌍 Cas d'Usage par Pays

### 🇨🇱 Chili - Pilote Nouvelle Version

- Permis de construire selon OGUC
- Brevets commerciaux
- Certificats d'informations préalables
- Intégration avec SII et Registre Civil

### 🇲🇽 Mexique - Version Classique

- Permis municipaux
- Licences commerciales
- Certificats de développement urbain

## 🛠️ Démarrage Rapide

1. **Exigences Système** : Docker, Node.js 18+, Python 3.13
2. **Installation** : Cloner le dépôt et exécuter la configuration
3. **Configuration** : Adapter pour votre municipalité
4. **Déploiement** : Configuration Docker prête pour la production

## 📖 Structure de la Documentation

Cette documentation est organisée en :

- **Prise en Main** : Installation et configuration
- **Adaptation Urbaine** : Implémentations spécifiques par pays
- **Développement** : Documentation API et composants
- **Déploiement** : Guides de production

## 🤝 Communauté Mondiale

Visor Urbano est conçu pour la réplication internationale avec :

- Support multi-langues (Espagnol, Anglais, Français, Portugais)
- Cadres juridiques adaptables
- Guides d'implémentation régionaux
- Communauté de développement active

---

Prêt à commencer ? Consultez notre [guide de configuration rapide](./quick-setup) ou parcourez les implémentations spécifiques pour votre région.
