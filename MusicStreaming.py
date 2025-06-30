from typing import List, Dict
from uuid import uuid4

# --- Models ---

class Song:
    def __init__(self, title: str, artist: str, album: str, genre: str, duration: int):
        self.id = str(uuid4())
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.duration = duration  # in seconds

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.album})"

class Playlist:
    def __init__(self, name: str):
        self.id = str(uuid4())
        self.name = name
        self.songs: List[Song] = []

    def add_song(self, song: Song):
        self.songs.append(song)

    def remove_song(self, song_id: str):
        self.songs = [s for s in self.songs if s.id != song_id]

class User:
    def __init__(self, name: str, email: str):
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.playlists: List[Playlist] = []
        self.history: List[str] = []  # song ids

# --- Core Components ---

class MusicPlayer:
    def __init__(self):
        self.current_song: Song = None
        self.current_position = 0  # seconds

    def play(self, song: Song):
        self.current_song = song
        self.current_position = 0
        print(f"🎵 Now playing: {song}")

    def pause(self):
        print(f"⏸️ Paused: {self.current_song.title} at {self.current_position}s")

    def skip(self):
        print("⏭️ Skipped current song.")
        self.current_song = None
        self.current_position = 0

    def seek(self, seconds: int):
        if self.current_song and 0 <= seconds <= self.current_song.duration:
            self.current_position = seconds
            print(f"⏩ Seeked to {seconds}s in {self.current_song.title}")

class RecommendationEngine:
    def recommend(self, user: User, all_songs: List[Song]) -> List[Song]:
        preferred_genres = set()
        for song_id in user.history:
            song = next((s for s in all_songs if s.id == song_id), None)
            if song:
                preferred_genres.add(song.genre)
        return [s for s in all_songs if s.genre in preferred_genres]

# --- Service Layer ---

class MusicService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.songs: Dict[str, Song] = {}
        self.player = MusicPlayer()

    def register_user(self, name: str, email: str) -> str:
        user = User(name, email)
        self.users[user.id] = user
        return user.id

    def add_song(self, title, artist, album, genre, duration) -> str:
        song = Song(title, artist, album, genre, duration)
        self.songs[song.id] = song
        return song.id

    def search_songs(self, keyword: str) -> List[Song]:
        return [song for song in self.songs.values() if keyword.lower() in song.title.lower()]

    def create_playlist(self, user_id: str, playlist_name: str):
        playlist = Playlist(playlist_name)
        self.users[user_id].playlists.append(playlist)

    def play_song(self, user_id: str, song_id: str):
        song = self.songs.get(song_id)
        if song:
            self.player.play(song)
            self.users[user_id].history.append(song_id)

    def get_recommendations(self, user_id: str):
        engine = RecommendationEngine()
        return engine.recommend(self.users[user_id], list(self.songs.values()))

# --- Sample Usage ---

if __name__ == "__main__":
    service = MusicService()

    # Register user
    user_id = service.register_user("Alice", "alice@example.com")

    # Add songs
    id1 = service.add_song("Blinding Lights", "The Weeknd", "After Hours", "Pop", 200)
    id2 = service.add_song("Save Your Tears", "The Weeknd", "After Hours", "Pop", 210)
    id3 = service.add_song("Believer", "Imagine Dragons", "Evolve", "Rock", 180)

    # Play and seek
    service.play_song(user_id, id1)
    service.player.seek(45)
    service.player.pause()

    # Playlist
    service.create_playlist(user_id, "Favorites")
    playlist = service.users[user_id].playlists[0]
    playlist.add_song(service.songs[id2])
    playlist.add_song(service.songs[id3])

    # Recommendations
    print("\nRecommended Songs:")
    recs = service.get_recommendations(user_id)
    for song in recs:
        print("-", song)
