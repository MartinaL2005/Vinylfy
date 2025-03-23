from flask import Flask, render_template, jsonify
from spotify_auth import get_current_song

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/song')
def song():
    try:
        song, artist, album_cover_url = get_current_song()
        return jsonify({'song': song, 'artist': artist, 'cover': album_cover_url})
    except:
        return jsonify({'error': 'No song currently playing'})

if __name__ == '__main__':
    app.run(debug=True)
