# OpenShelf - Peer-to-Peer Community Book Archive

OpenShelf is a lightweight, high-contrast digital library application designed for students to seamlessly share and query open-access educational resources. Built using Python and Flask, this platform operates with zero registration barriers, allowing instant discovery and crowdsourced document archiving.

## 🚀 Live Demo
Access the live production application here: `https://SivabharathiRamesh.pythonanywhere.com`

## ✨ Core Features
* **Zero-Barrier Metadata Querying:** Optimized SQLite search engine allowing immediate filtering by title, author, or custom search keywords.
* **Interactive Drag & Drop Ingestion:** Full asynchronous frontend interface supporting native `.pdf` document file uploads.
* **Persistent Distributed Storage:** Powered by a persistent server-side file system ensuring uploaded assets do not vanish over time.

## 🛠️ Tech Stack & Architecture
* **Backend Framework:** Python 3.10 + Flask 3.0.3
* **Database Engine:** SQLite3 (Relational mapping for tracking titles, authors, editions, and keywords)
* **Frontend Design:** Vanilla HTML5, CSS3 (Structured Grid System), and JavaScript (Drag & Drop DOM APIs)
* **Production Deployment:** PythonAnywhere Web WSGI Pipeline
