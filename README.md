# 🌌 Nexus AI Assistant - Version Améliorée

Une plateforme IA multimodale complète avec design premium et historique des conversations.

## ✨ Fonctionnalités

- ✅ **2 Modèles IA Puissants**
  - 🎨 **Molmo 2 8B** : Expert en vision et analyse d'images
  - 🧠 **GPT-OSS-120B (DeepSeek)** : Titan du texte pour raisonnement complexe

- ✅ **Interface Premium**
  - Design néon cyan/bleu avec dégradés
  - Polices Inter pour une typographie moderne
  - Effets de lueur et animations fluides
  - Mode sombre optimisé

- ✅ **Historique & Sauvegarde**
  - Sauvegarde automatique des conversations
  - Historique complet avec timestamps
  - Export en Markdown

- ✅ **Streaming en Temps Réel**
  - Réponses qui s'affichent au fur et à mesure
  - Expérience utilisateur fluide

- ✅ **100% Gratuit**
  - Utilise les modèles gratuits d'OpenRouter
  - Aucun coût caché

## 🚀 Installation Locale

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Configuration

Créez un fichier `.streamlit/secrets.toml` :

```toml
OPENROUTER_API_KEY = "sk-or-v1-YOUR_API_KEY_HERE"
```

## 📦 Déploiement sur Render

1. Poussez le code sur GitHub
2. Allez sur [render.com](https://render.com)
3. Créez un nouveau Web Service
4. Configurez :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Ajoutez la variable d'environnement `OPENROUTER_API_KEY`

## 📝 Utilisation

1. **Sélectionnez un modèle** dans la sidebar
2. **Posez votre question** dans la zone de chat
3. **Pour Molmo** : Uploadez une image pour l'analyse
4. **Sauvegardez** vos conversations
5. **Exportez** en Markdown depuis l'historique

## 🎨 Design

- **Couleurs** : Dégradés cyan (#00d4ff) et bleu (#0080ff)
- **Typographie** : Police Inter
- **Animations** : Transitions fluides et effets de lueur
- **Mode** : Sombre optimisé pour les yeux

## 📞 Support

Pour toute question ou amélioration, consultez le dépôt GitHub.

---

**Nexus AI Framework v3.0** | Sécurisé & Optimisé | Amélioré par Manus
