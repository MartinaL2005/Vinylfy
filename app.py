from flask import Flask, jsonify, render_template
from flask_cors import CORS
from spotify_auth import get_current_song

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/song')
def song():
    song, artist, cover = get_current_song()
    return jsonify({"song": song, "artist": artist, "cover": cover})

if __name__ == '__main__':
    app.run(debug=True)
