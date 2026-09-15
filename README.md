# 🎯 VALORANT TRACKER (Flask + HTML/CSS/JS)

Application web de suivi de statistiques et d'historique de parties pour Valorant, conçue en **Python (Flask)** avec une interface moderne aux couleurs officielles de Valorant en **HTML5 / CSS3 / Vanilla JavaScript**.

![Valorant Tracker](https://media.valorant-api.com/maps/7eae254d-459c-6c7c-f3b1-1294027ab989/splash.png)

## ✨ Fonctionnalités

- **Recherche par Riot ID** : Entrez `Pseudo#TAG` et sélectionnez votre région (`EU`, `NA`, `AP`, `KR`, `LATAM`, `BR`).
- **Fiche Joueur & Rang** :
  - Carte de joueur officielle et niveau de compte.
  - Badge du rang actuel (Fer à Radiant) avec barre de progression des RR (0 à 100 RR) et delta du dernier match.
  - Meilleur rang historique (Peak rank).
- **Statistiques Globales & Récents** :
  - K/D Ratio
  - Taux de victoire (Winrate %)
  - Taux de tirs à la tête (Headshot %)
  - Score de combat moyen (ACS)
- **Historique des Matchs** :
  - Carte jouée, mode (Compétitif, Non-classé), résultat (Victoire / Défaite / Égalité).
  - Agent joué avec portrait officiel.
  - Score final des manches (ex: 13-9).
  - K/D/A, ratio, ACS et HS%.
- **Tableau des scores complet (Modal 10 joueurs)** :
  - Détail manche par manche, équipes Bleue et Rouge avec tous les joueurs, leurs agents, rangs et scores.
- **Partage Facile avec Vos Amis** :
  - Bouton de copie en 1 clic.
  - Support des URLs directes : `/?name=TenZ&tag=SEN&region=na`.
- **Mode Démo & Double Support API** :
  - Intègre l'API **HenrikDev** (recommandée pour accéder aux matchs sans restriction Riot).
  - Support de l'API officielle **Riot Games**.
  - Mode démo ultra-réaliste actif par défaut si aucune clé n'est fournie.

---

## 🚀 Démarrage Rapide en Local

1. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurer les clés API (Optionnel) :**
   - Copiez `.env.example` en `.env` :
     ```bash
     copy .env.example .env
     ```
   - Renseignez votre `HENRIK_API_KEY` si vous en avez une. Sinon, l'application fonctionnera en mode démo.

3. **Lancer le serveur :**
   ```bash
   python app.py
   ```

4. **Accéder à l'application :**
   Ouvrez votre navigateur sur [http://localhost:5000](http://localhost:5000).

---

## 🌐 Hébergement Gratuit (Render.com)

Pour héberger ce site gratuitement et le partager avec vos amis :
Consultez le guide complet dans le fichier **[TUTORIEL_HEBERGEMENT.md](TUTORIEL_HEBERGEMENT.md)** !
