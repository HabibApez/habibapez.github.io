# Habib Apez Portfolio (GitHub Pages + Jekyll)

Professional portfolio site for Habib Alejandro Apez Gonzalez, built for deployment on GitHub Pages at <https://habibapez.github.io>.

## Stack

- Jekyll 4
- Minimal Mistakes theme (Bundler-managed)
- Markdown-first content model for easy updates
- GitHub Actions build, internal-link check, and Pages deployment

## Repository Structure

- `_config.yml`: global site configuration, plugins, collections, and SEO metadata
- `_pages/`: static pages (About, Projects, Research, Blog, CV, Contact)
- `_projects/`: project detail pages (collection)
- `_posts/`: blog posts
- `assets/css/main.scss`: design overrides and responsive styling
- `assets/js/scroll-fade.js`: lightweight reveal animation
- `assets/images/`: favicon and placeholder media
- `assets/docs/Habib_Apez_CV.pdf`: downloadable CV file
- `scripts/check_internal_links.rb`: generated-site internal link validation
- `scripts/create_social_thumbnail.ps1`: regenerates the LinkedIn/Open Graph card
- `.github/workflows/pages.yml`: continuous integration and GitHub Pages deployment

## Local Setup

1. Install Ruby + Bundler.
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Run locally:
   ```bash
   bundle exec jekyll serve
   ```
4. Open http://localhost:4000

## Validation

Build the production site and check all generated internal links:

```bash
JEKYLL_ENV=production bundle exec jekyll build
ruby scripts/check_internal_links.rb _site
```

The Sass configuration suppresses deprecation warnings originating inside Minimal Mistakes. The custom converter extension in `_plugins/sass_deprecation_filter.rb` also filters the two known `@import` notices required by the Minimal Mistakes 4.x entry points. Other project-owned Sass warnings remain visible.

Regenerate the 1200×627 social thumbnail on Windows after changing its text or design:

```powershell
.\scripts\create_social_thumbnail.ps1
```

## Deployment (GitHub Pages)

1. Push this repository to a public GitHub repository named exactly `habibapez.github.io`.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Push to `main`, or manually start the **Build, check, and deploy Jekyll site** workflow.
4. The workflow builds the site and checks internal links before deployment. Pull requests run the same checks without deploying.
5. After the workflow succeeds, open <https://habibapez.github.io>.

## Content Editing Guide

### Add a new blog post

1. Create a file in `_posts/` named `YYYY-MM-DD-title.md`.
2. Add front matter and markdown content.

### Add a new project

1. Create a file in `_projects/`.
2. Include fields used by the project cards:
   - `title`
   - `excerpt`
   - `tech_stack` (list)
   - `thumbnail`
   - `github_repo`
   - `live_demo`
   - `order`
   - `phase` (`completed`, `in-progress`, or `planned`)
   - `status`
   - `last_updated`

Use `phase` to place completed work before planned or in-progress projects. The `order` value controls ordering within that section. Use `last_updated` as the date when the portfolio entry or its evidence was last reviewed—not the project start date. Keep the field because it communicates maintenance status. Leave `github_repo` and `live_demo` empty until public artifacts exist, and mark future work as `Planned`.

Project claims should distinguish clearly between:

- **Implemented:** public code and measured results are available.
- **Historical research:** work was completed previously, but artifacts may be unavailable.
- **Planned:** methodology and evaluation criteria are a roadmap, not completed results.

## Notes

- Sitemap is generated at `/sitemap.xml`.
- Feed is generated at `/feed.xml`.
- Category and tag archives are generated at `/categories/` and `/tags/`.
- Favicon is `assets/images/favicon.svg`.
- Design palette:
   - Background: `#f3f7fb`
   - Surface: `#ffffff`
   - Text: `#17314d`
   - Heading: `#0f2235`
   - Accent: `#007a69`
   - Link: `#0f5f8f`
