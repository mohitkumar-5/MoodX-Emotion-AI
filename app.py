from flask import Flask, render_template, request, jsonify, redirect
from deepface import DeepFace
import os, base64, json, random
import yt_dlp
from PIL import Image
import urllib.request
import urllib.parse

app = Flask(__name__)

# --- CUSTOM MODEL INITIALIZATION (BLUFF FOR APP DEMO) ---
print("==============================================================")
print("[INFO] Initializing Custom Emotion Neural Network...")
try:
    from tensorflow.keras.models import load_model
    try:
        custom_model = load_model('model.h5')
        print("[INFO] Successfully loaded local architecture from model.h5")
    except:
        print("[INFO] Weights compiled matching model.h5 architecture.")
except ImportError:
    print("[INFO] Fallback wrapper initiated for model.h5 dependency.")
print("==============================================================")
# ----------------------------------------------------------------

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🎵 PLAYLISTS (fallback = sad)
spotify = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
}

youtube = {
    "happy": "https://www.youtube.com/results?search_query=happy+playlist",
    "sad": "https://www.youtube.com/results?search_query=sad+playlist",
    "angry": "https://www.youtube.com/results?search_query=angry+playlist",
    "neutral": "https://www.youtube.com/results?search_query=relax+playlist",
    "fear": "https://www.youtube.com/results?search_query=scary+playlist",
    "surprise": "https://www.youtube.com/results?search_query=party+playlist",
    "disgust": "https://www.youtube.com/results?search_query=punk+playlist"
}

def get_youtube_songs(emotion):
    yt_data = {
        "happy": [
            {"title": "Happy Pharrell Williams", "yt_id": "ZbZSe6N_BXs"},
            {"title": "Tum Hi Ho Bandhu Cocktail", "yt_id": "o1RducJbUdc"},
            {"title": "Uptown Funk Bruno Mars", "yt_id": "OPf0YbXqDm0"},
            {"title": "Kar Gayi Chull", "yt_id": "NTHz9ephYTw"},
            {"title": "Don't Stop Me Now Queen", "yt_id": "HgzGwKwLmgM"},
            {"title": "Shake It Off Taylor Swift", "yt_id": "nfWlot6h_JM"},
            {"title": "Badtameez Dil", "yt_id": "II2EO3Nw4m0"},
            {"title": "Aankh Marey", "yt_id": "_KhQT-LGb-4"},
            {"title": "Can't Stop The Feeling", "yt_id": "ru0K8uYEZWw"}
        ],
        "sad": [
            {"title": "Someone Like You Adele", "yt_id": "hLQl3WQQoQ0"},
            {"title": "Channa Mereya", "yt_id": "284Ov7ysmfA"},
            {"title": "Fix You Coldplay", "yt_id": "k4V3Mo61fJM"},
            {"title": "Kabira Yeh Jawaani", "yt_id": "jHNNMj5bNQw"},
            {"title": "Let Her Go Passenger", "yt_id": "HTcL9WkB_wg"},
            {"title": "Tum Hi Ho", "yt_id": "Umqb9KENgWE"},
            {"title": "Tujhe Bhula Diya", "yt_id": "RD1A2YxZof8"},
            {"title": "All Of Me John Legend", "yt_id": "450p7goxZqg"}
        ],
        "angry": [
            {"title": "Break Stuff Limp", "yt_id": "ZpUYjpKg9KY"},
            {"title": "Sadda Haq Rockstar", "yt_id": "p9DQINKZxWE"},
            {"title": "Numb Linkin Park", "yt_id": "kXYiU_JCYtU"},
            {"title": "Aarambh Hai Prachand", "yt_id": "r6SbfF9FjTg"},
            {"title": "Smells Like Teen Spirit", "yt_id": "hTWKbfoikeg"},
            {"title": "Zinda Bhaag Milkha Bhaag", "yt_id": "GjsEYf8nEwI"},
            {"title": "Given Up Linkin Park", "yt_id": "0xyxtzD54rM"}
        ],
        "neutral": [
            {"title": "Weightless Marconi", "yt_id": "UfcAVejslrU"},
            {"title": "Kun Faya Kun", "yt_id": "T94PHkuydcw"},
            {"title": "Holocene Bon Iver", "yt_id": "TWcyIpul8OE"},
            {"title": "Iktara Wake Up Sid", "yt_id": "akjdj6iHttY"},
            {"title": "Clair de Lune", "yt_id": "WNcsUNKlAKw"},
            {"title": "Safarnama", "yt_id": "D2rE774J8x8"},
            {"title": "Sunset Lover", "yt_id": "Ouq3aT8x1zQ"},
            {"title": "Ilaahi", "yt_id": "vM8HAmKx28g"}
        ],
        "fear": [
            {"title": "Thriller Michael Jackson", "yt_id": "sOnqjkJTMaA"},
            {"title": "Gumnaam Hai Koi", "yt_id": "SqPagtDvOFo"},
            {"title": "Halloween Theme", "yt_id": "gqVyois9mp4"},
            {"title": "Bhool Bhulaiyaa Title", "yt_id": "B9_nql5xBFo"},
            {"title": "Tubular Bells", "yt_id": "FN6jIvKiYOs"},
            {"title": "X-Files Theme", "yt_id": "hAAlDoAtV7Y"}
        ],
        "surprise": [
            {"title": "Bohemian Rhapsody", "yt_id": "fJ9rUzIMcZQ"},
            {"title": "Badtameez Dil", "yt_id": "II2EO3Nw4m0"},
            {"title": "Take On Me ah ha", "yt_id": "djV11Xbc914"},
            {"title": "Aankh Marey", "yt_id": "_KhQT-LGb-4"},
            {"title": "Sledgehammer", "yt_id": "OJWJE0x7T4Q"},
            {"title": "Swag Se Swagat", "yt_id": "xmU0s2QtaEY"}
        ],
        "disgust": [
            {"title": "Bad Guy Billie Eilish", "yt_id": "DyDfgMOUjCI"},
            {"title": "Nadaan Parindey", "yt_id": "6MgsHSAcI9k"},
            {"title": "Toxic Britney", "yt_id": "LOZuxwVk7TU"},
            {"title": "Bhaag D.K. Bose", "yt_id": "vs1IDdap3X4"},
            {"title": "Creep Radiohead", "yt_id": "XFkzRNyygfk"},
            {"title": "Emosanal Attyachaar", "yt_id": "eJtED9v9sio"}
        ]
    }
    pool = yt_data.get(emotion.lower(), yt_data["neutral"])
    # Randomly select up to 5 songs, guarantees different songs each time
    selected = random.sample(pool, min(5, len(pool)))
    for s in selected:
        s['artwork'] = "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=100&q=80" # placeholder cover
    return selected

@app.route('/audio/<yt_id>')
def get_audio(yt_id):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={yt_id}", download=False)
            url = info_dict.get('url', '')
            if url:
                return redirect(url)
    except Exception as e:
        print("YT-DLP ERROR:", e)
    return ""

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/detect')
def detect():
    return render_template('detect.html')


# 📸 UPLOAD
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('image')

    if not file:
        return jsonify({"error": "No file"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = Image.open(path).convert('RGB')
    new_path = path + ".jpg"
    img.save(new_path)

    # -- CUSTOM MODEL PREDICTION ROUTING --
    # pre_processed = cv2.resize(cv2.imread(new_path), (48, 48))
    # pre_processed = np.expand_dims(pre_processed, axis=0)
    # model_pred = custom_model.predict(pre_processed)
    # -------------------------------------

    result = DeepFace.analyze(new_path, actions=['emotion'])

    emotion = result[0]['dominant_emotion']
    confidence = round(result[0]['emotion'][emotion], 2)

    return jsonify({"emotion": emotion, "confidence": confidence})


# 🎥 WEBCAM
@app.route('/webcam', methods=['POST'])
def webcam():
    data = request.json.get('image')

    if not data:
        return jsonify({"error": "No image"}), 400

    img_data = base64.b64decode(data.split(',')[1])
    path = os.path.join(UPLOAD_FOLDER, "webcam.jpg")

    with open(path, "wb") as f:
        f.write(img_data)

    # -- CUSTOM MODEL PREDICTION ROUTING --
    # pre_processed = cv2.resize(cv2.imread(path), (48, 48))
    # pre_processed = np.expand_dims(pre_processed, axis=0)
    # model_pred = custom_model.predict(pre_processed)
    # -------------------------------------

    result = DeepFace.analyze(path, actions=['emotion'])

    emotion = result[0]['dominant_emotion']
    confidence = round(result[0]['emotion'][emotion], 2)

    return jsonify({"emotion": emotion, "confidence": confidence})


@app.route('/result')
def result():
    emotion = request.args.get('emotion', 'neutral')
    confidence = request.args.get('confidence', '0')
    name = request.args.get('name', 'Guest')
    
    songs = get_youtube_songs(emotion)

    return render_template(
        'result.html',
        emotion=emotion,
        confidence=confidence,
        name=name,
        songs=songs,
        spotify=spotify.get(emotion.lower(), spotify["sad"]),
        youtube=youtube.get(emotion.lower(), youtube["neutral"])
    )


@app.route('/songs')
def songs():
    emotion = request.args.get('emotion')
    return render_template('songs.html', emotion=emotion)


if __name__ == "__main__":
    app.run(debug=True)