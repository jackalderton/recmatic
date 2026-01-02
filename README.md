# Recmatic – Content Recommendation Template Generator

Recmatic is a Streamlit-based tool that automates the creation of content recommendation templates.
It crawls an input URL, extracts key elements (headings, body content, schema, etc.) and outputs them into a formatted Word template for editing.

## Features

* Password-protected Streamlit app (with session persistence).
* Extracts and cleans page HTML:

  * Headings (h1–h6)
  * Paragraphs
  * Images (with alt text, optional sources)
  * JSON-LD schema (if present)
* Optional settings (exclude selectors, strip before first `<h1>`, annotate links, etc.).
* Outputs into a `.docx` template with placeholders replaced.
* Saves time by automating manual copy/paste and formatting.

## Tech stack

* Frontend: Streamlit
* Backend: Python (`requests`, `BeautifulSoup`, `python-docx`)
* Deployment: Currently containerised and deployed via Google Cloud Run

## Requirements

* Python 3.11+
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```
* Run locally:

  ```bash
  streamlit run app.py
  ```

The app will start on [http://localhost:8501](http://localhost:8501).

---

### Note on Local Development

This app uses **Google Cloud Run Secret Manager** to store the login password.
When running locally, the `APP_PASSWORD` environment variable will not be available unless you:

1. Remove or bypass the password check in `app.py`, **or**
2. Manually set a password in your local environment, e.g.:

   ```bash
   export APP_PASSWORD="yourpassword"
   ```

---

## Deployment

* A `Dockerfile` is included for containerised deployment.
* `.devcontainer/` folder is included for Codespaces/VS Code Dev Containers (optional, for development convenience).
