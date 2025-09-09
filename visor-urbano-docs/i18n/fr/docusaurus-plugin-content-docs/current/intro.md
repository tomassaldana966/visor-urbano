---
sidebar_position: 1
---

# Bienvenue à Visor Urbano

Découvrez **Visor Urbano** - le système intégral de gestion de planification urbaine municipale.

## Commencer

Démarrez votre implémentation en **créant une nouvelle instance**.

Ou **essayez Visor Urbano immédiatement** avec nos **[tutoriels de configuration rapide](./getting-started/quick-setup.md)**.

### Ce dont vous aurez besoin

- [Node.js](https://nodejs.org/en/download/) version 18.0 ou supérieure
- [Python](https://python.org/downloads/) version 3.8 ou supérieure
- Un serveur avec les spécifications minimales requises

## Générer une nouvelle installation

Exécutez la commande d'installation pour générer un nouveau site Visor Urbano :

```bash
git clone https://github.com/Delivery-Associates/visor-urbano.git
cd visor-urbano
npm install
```

Vous pouvez taper cette commande dans l'invite de commande, Powershell, Terminal, ou tout autre terminal intégré de votre éditeur de code.

La commande installe également toutes les dépendances nécessaires pour exécuter Visor Urbano.

## Démarrer votre installation

Exécutez le serveur de développement :

```bash
npm run start
```

La commande `npm run start` construit votre site localement et le sert via un serveur de développement, prêt à être visualisé sur http://localhost:3000/.

Ouvrez `docs/intro.md` (cette page) et modifiez quelques lignes : le site **se recharge automatiquement** et affiche vos modifications.

## Et ensuite ?

- [Configuration Rapide](./getting-started/quick-setup.md) : Configurez votre environnement de développement
- [Exigences Système](./getting-started/system-requirements.md) : Vérifiez les spécifications techniques
- [Intégration API](./development/api-integration.md) : Documentation technique pour développeurs
- [Adaptation Urbaine](./city-adaptation/integration-chile.md) : Guides spécifiques par région

Des questions ? [Rejoignez notre communauté de développeurs](https://github.com/Delivery-Associates/visor-urbano/discussions).
