# 🖼️ FaceRestore AI — GFPGAN Face Enhancement Web App

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Replicate](https://img.shields.io/badge/Replicate-API-6B46C1?style=for-the-badge&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A Flask web application that restores and enhances face photos using GFPGAN via the Replicate API — upload up to 20 images and download all enhanced results as a single ZIP file.**

[Features](#-features) • [How It Works](#-how-it-works) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security)

</div>

---

## 🌟 Overview

FaceRestore AI lets users upload old, blurry, or low-quality face photos and receive AI-enhanced versions in seconds. It leverages **GFPGAN (Generative Facial Prior GAN)** — a state-of-the-art face restoration model — through the Replicate API, wrapped in a clean Flask web interface. Batch processing is supported for up to 20 images per session, with all results packaged into a convenient ZIP download.

---

## ✨ Features

- **Batch Upload** — process up to 20 images in a single session
- **GFPGAN Enhancement** — uses a production-grade face restoration model via Replicate
- **ZIP Download** — all enhanced images bundled into one download
- **Session Isolation** — each upload gets a unique UUID session folder, preventing file conflicts
- **Format Support** — accepts PNG, JPG, and JPEG files
- **File Size Limit** — 16MB max per upload for safety
- **Flash Messaging** — clear user feedback for errors and invalid files
- **Auto Cleanup** — temporary session files removed after processing

---

## 🔍 How It Works

```
User uploads images (up to 20)
        ↓
Flask saves files to unique session folder
        ↓
Each image encoded to Base64 data URI
        ↓
Replicate API → GFPGAN model (face restoration)
        ↓
Poll prediction status until complete
        ↓
Download enhanced image from Replicate output URL
        ↓
Package all enhanced images into ZIP
        ↓
Serve ZIP to user & clean up temp files
```

### GFPGAN Model

GFPGAN is a practical algorithm for real-world blind face restoration. It leverages rich and diverse priors encapsulated in a pretrained face GAN to restore degraded faces with high fidelity.

| Property | Value |
|---|---|
| Model | GFPGAN |
| Provider | Replicate API |
| Input | Base64-encoded image |
| Output | Enhanced image URL |
| Max images | 20 per session |
| Max file size | 16MB |

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Replicate API key ([get one here](https://replicate.com))

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/facerestore-ai.git
cd facerestore-ai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```txt
flask
replicate
requests
python-dotenv
werkzeug
```

---

## 🔐 Security

Create a `.env` file in the project root:

```env
REPLICATE_API_TOKEN=your_replicate_api_token_here
```

Add `.env` to your `.gitignore`:

```
.env
uploads/
outputs/
*.zip
```

> ⚠️ **Never commit your API token to version control.** Always use environment variables.

---

## 🚀 Usage

### Start the Server

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

### Using the Web Interface

1. Open `http://localhost:5000` in your browser
2. Select up to **20 face images** (PNG, JPG, or JPEG)
3. Click **Upload & Enhance**
4. Wait for GFPGAN to process each image (polling every 2 seconds)
5. Your browser will automatically download `enhanced_images.zip`

### File Naming Convention

| Original | Enhanced |
|---|---|
| `photo.jpg` | `enhanced_photo.jpg` |
| `portrait.png` | `enhanced_portrait.png` |

---

## 📁 Project Structure

```
facerestore-ai/
│
├── app.py                  # Flask application
│   ├── upload_images()     # Main route (GET + POST)
│   └── allowed_file()      # File extension validator
│
├── templates/
│   └── index.html          # Upload form template
│
├── uploads/                # Temporary upload storage (auto-created)
│   └── <session-uuid>/     # Per-session isolation
│
├── outputs/                # Enhanced image output (auto-created)
│   └── <session-uuid>/     # Per-session enhanced files
│
├── .env                    # API keys (gitignored)
└── requirements.txt
```

---

## 🌐 Template

Create `templates/index.html` with a basic upload form:

```html
<!DOCTYPE html>
<html>
<head><title>FaceRestore AI</title></head>
<body>
  <h1>🖼️ FaceRestore AI</h1>

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for message in messages %}
        <p style="color: red;">{{ message }}</p>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="images" multiple accept=".png,.jpg,.jpeg" required>
    <br><br>
    <button type="submit">✨ Enhance Faces</button>
  </form>

  <p><small>Upload up to 20 images (PNG, JPG, JPEG). Max 16MB total.</small></p>
</body>
</html>
```

---

## ⚙️ Configuration

| Config Key | Default | Description |
|---|---|---|
| `UPLOAD_FOLDER` | `uploads/` | Temporary image storage |
| `OUTPUT_FOLDER` | `outputs/` | Enhanced image storage |
| `MAX_CONTENT_LENGTH` | 16MB | Max upload size |
| `SECRET_KEY` | Custom | Flask session security |
| Polling interval | 2 seconds | Replicate status check delay |

---

## 📈 Roadmap

- [ ] Drag-and-drop upload UI with preview thumbnails
- [ ] Real-time progress bar per image
- [ ] Side-by-side before/after comparison view
- [ ] Support for colorization and super-resolution models
- [ ] User accounts with processing history
- [ ] Deploy to Railway / Render / Heroku

---

## 🤝 Contributing

```bash
# Fork and clone
git clone https://github.com/yourusername/facerestore-ai.git

# Create feature branch
git checkout -b feature/your-feature

# Commit and push
git commit -m "Add: your feature"
git push origin feature/your-feature
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgements

- [GFPGAN](https://github.com/TencentARC/GFPGAN) — Tencent ARC face restoration model
- [Replicate](https://replicate.com/) — Cloud AI model hosting
- [Flask](https://flask.palletsprojects.com/) — Python web framework

---

<div align="center">
  <b>Restore the past. Enhance the present. 🖼️✨</b>
</div>
