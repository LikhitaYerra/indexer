# GitHub Pages Setup Guide

Follow these steps to deploy your Index Generator website to GitHub Pages.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `indexer` (or your preferred name)
4. Keep it **Public** (required for free GitHub Pages)
5. Don't initialize with README (we already have one)
6. Click **Create repository**

## Step 2: Push Your Code

Run these commands in your terminal:

```bash
cd /Users/likhitayerra/indexer

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/indexer.git

# Push your code
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section (in the left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

## Step 4: Access Your Site

After a few minutes, your site will be live at:

```
https://YOUR_USERNAME.github.io/indexer/
```

GitHub will show you the URL in the Pages settings.

## Updating Your Site

Whenever you make changes:

```bash
git add .
git commit -m "Update website"
git push
```

GitHub Pages will automatically rebuild and deploy your site within a few minutes.

## Custom Domain (Optional)

To use a custom domain like `indexer.yourname.com`:

1. Buy a domain from a registrar
2. In your repository Settings → Pages, add your custom domain
3. Configure DNS records with your registrar:
   - Add a CNAME record pointing to `YOUR_USERNAME.github.io`
4. Wait for DNS propagation (can take up to 48 hours)

## Troubleshooting

**Site not showing up?**
- Wait 5-10 minutes after enabling Pages
- Check the Pages section shows a green checkmark
- Make sure files are in `/docs` folder
- Verify the repository is Public

**404 errors?**
- Check that `index.html` exists in `/docs`
- Ensure file names are lowercase
- Clear browser cache

**Changes not appearing?**
- Wait a few minutes for rebuild
- Do a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check the Actions tab for build status

## Preview Locally

Before pushing, preview your site locally:

```bash
cd docs
python3 -m http.server 8000
```

Then visit `http://localhost:8000`

---

**Note:** Update the GitHub repository URL in `index.html` to match your actual repository.
