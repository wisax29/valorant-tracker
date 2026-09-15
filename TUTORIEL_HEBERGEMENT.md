# 🚀 TUTORIEL : Comment Héberger et Partager Votre Tracker Valorant

Ce guide complet vous explique pas-à-pas comment mettre en ligne votre Tracker Valorant **gratuitement** sur Internet, pour que vous et vos amis puissiez consulter vos statistiques, historiques de parties et rangs depuis n'importe où (PC, tablette, smartphone) 24h/24 !

---

## Sommaire
1. [Comprendre les Clés API (Riot Games vs HenrikDev)](#1-comprendre-les-clés-api)
2. [Tester le Tracker en Local sur Votre PC](#2-tester-le-tracker-en-local)
3. [Mettre le Projet sur GitHub](#3-mettre-le-projet-sur-github)
4. [Déployer Gratuitement sur Render.com (Recommandé)](#4-déployer-sur-rendercom)
5. [Partager le Tracker avec Vos Amis](#5-partager-avec-vos-amis)
6. [Alternatives d'Hébergement](#6-alternatives-dhébergement)

---

## 1. Comprendre les Clés API

Pour afficher l'historique des matchs et le rang d'un joueur, il existe deux options :

### Option A : L'API HenrikDev (Fortement Recommandée ⭐)
- **Pourquoi ?** Riot Games bloque l'accès direct aux matchs (`val-match-v1`) pour les développeurs indépendants sans contrat commercial. HenrikDev fournit une API publique utilisée par toute la communauté Valorant.
- **Comment obtenir une clé gratuite :**
  1. Rendez-vous sur [docs.henrikdev.xyz](https://docs.henrikdev.xyz) ou rejoignez leur serveur Discord officiel.
  2. Allez dans le salon `#get-a-key` ou sur le dashboard développeur.
  3. Vous recevrez instantanément une clé API personnelle gratuite (30 requêtes/minute, largement suffisant pour vous et vos amis).

### Option B : L'API Officielle Riot Games
- **Lien :** [developer.riotgames.com](https://developer.riotgames.com/)
- **Utilité :** Permet de vérifier les pseudos, Riot ID (`puuid`) et le statut des serveurs. Pour les matchs, Riot demande une candidature d'entreprise avec authentification RSO (Riot Sign-On).

### Option C : Le Mode Démo Intégré (0 configuration)
- Votre application intègre un mode de données simulées ultra-réaliste (parties complètes, scores, maps, agents, rangs Radiant/Immortal). Même sans aucune clé API configurée, le tracker fonctionne immédiatement !

---

## 2. Tester le Tracker en Local

Avant d'héberger, vérifiez que tout fonctionne sur votre machine :

1. Ouvrez un terminal dans le dossier du projet (`c:\Users\wisax\Desktop\tracker valo`).
2. Installez les dépendances si ce n'est pas déjà fait :
   ```bash
   pip install -r requirements.txt
   ```
3. Créez votre fichier `.env` :
   - Dupliquez `.env.example` et renommez-le en `.env`.
   - Si vous avez votre clé HenrikDev, collez-la :
     ```env
     HENRIK_API_KEY=votre_cle_ici
     ```
4. Lancez le serveur Flask :
   ```bash
   python app.py
   ```
5. Ouvrez votre navigateur sur : **[http://localhost:5000](http://localhost:5000)**.
6. Testez une recherche (ex: `TenZ#SEN` ou cliquez sur le bouton "Test Démo Rapide").

---

## 3. Mettre le Projet sur GitHub

Pour que l'hébergeur cloud puisse récupérer votre code, la méthode la plus propre et automatisée est de le mettre sur **GitHub**.

1. Créez un compte gratuit sur [github.com](https://github.com) si vous n'en avez pas.
2. Créez un nouveau dépôt (Repository) vide nommé `mon-tracker-valo` (en mode Public ou Privé).
3. Dans votre terminal dans le dossier du projet, tapez ces commandes :
   ```bash
   git init
   git add .
   git commit -m "Premier commit du Tracker Valorant"
   git branch -M main
   git remote add origin https://github.com/VOTRE_PSEUDO_GITHUB/mon-tracker-valo.git
   git push -u origin main
   ```
*(Note : votre fichier `.env` ne sera jamais envoyé grâce au `.gitignore` de sécurité).*

---

## 4. Déployer sur Render.com (Gratuit & 24/7)

**Render** est l'un des meilleurs hébergeurs cloud gratuits pour les applications Python Flask :
- Hébergement 100% gratuit
- Certificat SSL automatique (URL sécurisée en `https://`)
- Redéploiement automatique dès que vous modifiez votre code sur GitHub

### Étapes :
1. Rendez-vous sur **[render.com](https://render.com)** et créez un compte (vous pouvez vous connecter directement avec votre compte GitHub).
2. Sur le tableau de bord, cliquez sur le bouton **New +** en haut à droite, puis sélectionnez **Web Service**.
3. Choisissez **Build and deploy from a Git repository** et connectez votre dépôt `mon-tracker-valo`.
4. Remplissez les champs de configuration :
   - **Name :** `mon-tracker-valo` (ou le nom de votre choix)
   - **Region :** `Frankfurt (EU Central)` (idéal si vous êtes en Europe)
   - **Branch :** `main`
   - **Language :** `Python 3`
   - **Build Command :** `pip install -r requirements.txt`
   - **Start Command :** `gunicorn app:app`
   - **Instance Type :** `Free` (0$/mois)
5. **Ajouter votre clé API dans les Variables d'Environnement :**
   - Descendez dans la section **Environment Variables**.
   - Cliquez sur **Add Environment Variable** :
     - **Key :** `HENRIK_API_KEY`
     - **Value :** `votre_clé_ici`
   - *(Optionnel)* Ajoutez aussi `DEFAULT_REGION` avec la valeur `eu`.
6. Cliquez sur le bouton **Create Web Service** tout en bas.

Render va installer les packages, configurer Gunicorn et démarrer votre application. En 2 à 3 minutes, votre site est en ligne avec une URL du type :
👉 **`https://mon-tracker-valo.onrender.com`**

---

## 5. Partager avec Vos Amis

### A. Le lien simple
Donnez simplement votre URL Render à vos potes :
`https://mon-tracker-valo.onrender.com`

### B. Le lien direct vers un profil (Super Pratique !)
L'application prend en charge les paramètres d'URL automatiques. Vous pouvez générer un lien qui ouvre directement les stats d'un joueur en envoyant :
`https://mon-tracker-valo.onrender.com/?name=PSEUDO&tag=TAG&region=eu`

*Exemple pour envoyer la fiche de TenZ à un pote :*
`https://mon-tracker-valo.onrender.com/?name=TenZ&tag=SEN&region=na`

Lorsque votre ami clique sur ce lien, le tracker se charge et lance immédiatement la recherche de son profil !

### C. Le bouton "Partager le Profil"
Directement dans l'interface du tracker, sous le pseudo du joueur, un bouton **"Partager le Profil"** permet de copier en 1 clic le lien direct dans le presse-papier.

---

## 6. Alternatives d'Hébergement

Si vous préférez une autre plateforme que Render :

- **Railway.app :** Très rapide, offre des crédits gratuits au départ. Il suffit de lier GitHub et Railway détecte automatiquement le `Procfile` et le `requirements.txt`.
- **Koyeb.com :** Excellent hébergeur cloud gratuit avec serveurs à Paris et Francfort, prise en charge native de Flask et Python.
- **PythonAnywhere.com :** Idéal pour exécuter du pur Flask sans conteneurisation, mais nécessite une configuration manuelle du fichier WSGI.

---

## 💡 Astuce Mobile
Vous et vos potes pouvez ouvrir le site sur votre smartphone (Chrome sur Android ou Safari sur iPhone) et faire **"Ajouter à l'écran d'accueil"**. Le site s'ouvrira alors en plein écran comme une véritable application Valorant mobile !
