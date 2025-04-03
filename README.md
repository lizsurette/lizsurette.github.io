# Liz Blanchard's Personal Website

A personal website built with Flask and Frozen-Flask for static site generation.

## Project Structure

```
.
├── app/                    # Flask application
│   ├── posts/             # Markdown blog posts
│   ├── static/            # Static assets (CSS, JS, images)
│   └── templates/         # HTML templates
├── _site/                 # Generated static site
├── app.py                 # Flask application
├── freeze.py              # Static site generator
├── requirements.txt       # Python dependencies
├── deploy.sh              # Deployment script
├── push.sh                # Git push script
└── serve.sh               # Local development server
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lizsurette/lizsurette.github.io.git
   cd lizsurette.github.io
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

1. Run the Flask development server:
   ```bash
   ./serve.sh
   ```

2. Generate the static site:
   ```bash
   python freeze.py
   ```

3. Test the static site locally:
   ```bash
   cd _site
   python -m http.server 8000
   ```

## Deployment

1. Push changes to GitHub:
   ```bash
   ./push.sh
   ```

2. Deploy to GitHub Pages:
   ```bash
   ./deploy.sh
   ```

## Features

- Blog posts written in Markdown
- Static site generation with Frozen-Flask
- Responsive design
- Interactive games (Hangman, Snake, Strands)
- Project showcase

## Adding Blog Posts

Create new blog posts in the `app/posts/` directory using Markdown format with YAML front matter:

```markdown
---
layout: post
title: Your Post Title
date: YYYY-MM-DD
categories: [Category1, Category2]
---

Your post content here in Markdown format.
```

## Deploying to GitHub Pages

This site is configured to automatically deploy to GitHub Pages using GitHub Actions.

### Manual Deployment

To manually generate the static site and test it locally:

```bash
python test_static.py
```

This will generate the static site in the `_site` directory and start a local server to test it.

### Automatic Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment process:

1. Installs dependencies
2. Generates the static site using Flask-Frozen
3. Deploys the static site to the gh-pages branch

You can also manually trigger the deployment from the Actions tab in the GitHub repository.
