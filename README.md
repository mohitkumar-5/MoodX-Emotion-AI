<div align="center">

# 🎵 MoodX - Emotion-Aware Soundtrack Engine

**MoodX** is a deep-learning-powered multimodal engine that reads human psychology and bridges it to audio frequencies. By evaluating micro-expressions through Convolutional Neural Networks, it actively synthesizes and links your visual state to dynamic audio libraries, balancing your cognitive load in real time.

[Features](#-features) •
[Technologies](#%EF%B8%8F-technologies) •
[Installation](#%EF%B8%8F-getting-started) 
</div>

---

## 🌟 Features

- **🧠 Neural Emotion Decoding:** Analyzes live facial features via webcam or image upload to instantly match a soundtrack to your expressions using DeepFace.
- **🎧 Adaptive Listening Engine:** Streams entirely curated YouTube audio dynamically using `yt-dlp` based exactly on detected mood frequencies without needing iTunes previews or API keys.
- **✨ Fluid UI/UX:** A state-of-the-art Aurora dark-mode UI with smart sticky scroll navigation, native glassmorphism filters, and a pure CSS/HTML5 dynamic audio canvas.
- **🔐 Privacy-First AI:** All sensory wavelength simulation models execute heavily on local architecture (via `.h5` model bypasses), ensuring complete privacy.
- **🔄 Simultaneous Execution Filtering:** Smart overlapping playback prevention seamlessly fades old tracks when initiating new moods. 

---

## 🛠️ Technologies

### **Frontend Interface**
- **HTML5 & CSS3:** Semantic markup and advanced CSS3 features (blur backdrop-filters, custom keyframes).
- **JavaScript (ES6):** Used for exclusive audio playback synchronization, smart scroll listeners, and real-time canvas waveform visualizers.
- **Jinja2:** Template rendering engine linked to the Flask backend.

### **Backend Server**
- **Python 3.x:** Core backend system.
- **Flask:** Lightweight, highly robust Python web framework routing neural detection metrics.
- **DeepFace / OpenCV / TensorFlow:** Under-the-hood engine used for extracting raw pixel data from live feeds and classifying 7 categorical emotional states.
- **yt-dlp:** Custom audio parser downloading real-time full-resolution audio packets from external CDNs.

---

## 📂 Complete File Structure

```text
ai_project/
│
├── app.py                 # Core routing and deep learning logic execution
├── model.h5               # Stored neural network compilation architectures
├── yt_data.json           # Local database mapping emotions safely to track IDs
├── requirements.txt       # Necessary python packaging
│
├── static/
│   ├── styles.css         # The master glassmorphic stylesheet
│   └── uploads/           # Ephemeral storage location for CV2 predictions
│
└── templates/
    ├── index.html         # Homepage and Neural Waveform Canvas
    ├── detect.html        # Live camera scanning UI
    └── result.html        # Dashboard generating playlists
```

---

## 🛠️ Getting Started

Follow these steps to deploy MoodX onto your local hardware.

### 1. Requirements Checklist
Ensure you have the following installed natively:
- **Python** (Specifically `3.8 - 3.10` for Keras compatibility).
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/MoodX.git
cd MoodX
```

### 3. Setup Virtual Environment
It is highly recommended to segregate the complex DeepFace packages into an isolated virtual environment.
**Windows:**
```bash
python -m venv my_envgpu
.\my_envgpu\Scripts\activate
```
**MacOS / Linux:**
```bash
python3 -m venv my_envgpu
source my_envgpu/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Server
```bash
python app.py
```
After executing, navigate your browser to `http://127.0.0.1:5000` to interact with the engine.

---

> Built with ❤️ by [Your Name]
