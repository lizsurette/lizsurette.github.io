# Liz Blanchard's Personal Website

A Flask-based personal website featuring a blog, projects showcase, and interactive games.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python app.py
```

The site will be available at http://localhost:5000

## Project Structure

- `app.py` - Main Flask application
- `app/templates/` - HTML templates
- `app/static/` - Static files (CSS, images, etc.)
- `app/posts/` - Markdown blog posts
- `requirements.txt` - Python dependencies

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

## Features

- Responsive design
- Blog with category support
- Project showcase
- Interactive games (Snake, Hangman, Strands)
- About page
- Social media links

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
