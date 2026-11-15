# SkinRx by Burds Family Practice: Static Website

A fast, self-contained static website for **SkinRx by Burds Family Practice** (`burdsskinrx.com`), the medical aesthetics clinic of Burds Family Practice serving Peosta, Dyersville, and the greater Dubuque area. Built with zero runtime CMS dependencies, self-hosted typography, and real clinic photography.

## Structure

```text
build.py            # builds 10 core pages (incl. 404 & privacy), sitemap.xml, robots.txt, 6 Learning Hub guides, and 12 Blog posts -> dist/
tools_emblem.py     # generates emblem-dark.svg, emblem-light.svg, favicon.svg, and hero-banner-bg.svg
src/layout.html     # shared header, navigation, JSON-LD schema, footer, and mobile booking bar
src/pages/*.html    # core pages (index, treatments, packages, skincare, financing, about, resources, contact, privacy, 404)
src/learn/*.html    # 6 native clinical comparison guides
src/blog/*.html     # 12 native patient education articles
src/assets/         # css, js, self-hosted woff2 fonts, clinic/team/results photos, SVG emblems, and vCard
dist/               # generated static site output
```

## Build & Preview

```bash
python3 tools_emblem.py   # regenerate SVG emblems and hero background
python3 build.py          # build all pages, sitemap.xml, and robots.txt into dist/
python3 build.py serve    # build and preview locally at http://localhost:8080
```

## Brand & Visual System

- **Palette**:
  - **Deep Espresso Ink**: `#26211F`
  - **Dusty Blush**: `#C3B1AC`
  - **Deep Mauve**: `#6E525C`
  - **Soft Sage**: `#BCCCC1`
  - **Soft Cream**: `#F5F2EF`
- **Self-Hosted Typography (`src/assets/fonts/`)**:
  - `Source Sans 3` (400, 400 italic) for body copy
  - `Cormorant Garamond` (500, 500 italic, 600) for editorial headings
  - `Josefin Sans` (400, 600) for navigation, labels, and buttons
  - `Allura` (400) for the script wordmark
- **Clinic & Brand Assets (`src/assets/img/`)**:
  - Official circular SkinRx seal (`brand-lockup-dark.png`) and vector emblems (`emblem-dark.svg`, `emblem-light.svg`, `favicon.svg`, `hero-banner-bg.svg`)
  - Clinic and skincare imagery (`hero-peosta.jpg`, `about-consult.jpg`, `about-care.jpg`, `skincare-products.jpg`, `skinrx-etagere.jpg`, `skinrx-shelf.jpg`, `front-desk.jpg`, `lobby.jpg`, `storefront.jpg`)
  - Five provider portraits in `src/assets/img/team/`
  - Sixteen real clinical before-and-after patient result photos in `src/assets/img/results/`

## Clinics & Integrations

- **Peosta Clinic**: 8411 Peosta Commercial Ct, Suite #8, Peosta, IA 52068 | (563) 588-6659
- **Dyersville Clinic**: 251 1st Ave E, Dyersville, IA 52040 | (563) 588-6659
- **Online Booking (Mangomint)**: `https://booking.mangomint.com/437183`
- **Gift Cards (Mangomint)**: `https://clients.mangomint.com/gift-cards/437183`
- **Cherry Financing**: `https://pay.withcherry.com/burdsfamilypractice`
- **SkinBetter Science Store**: Business Partner ID `0000252738`
