from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import csv
import math


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional adaptive taste weights — updated via feedback
    listened_genres: Dict[str, int] = field(default_factory=dict)
    liked_song_ids: List[int] = field(default_factory=list)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    # Scoring weights — tweak these to experiment!
    WEIGHT_GENRE = 3.0
    WEIGHT_MOOD = 2.5
    WEIGHT_ENERGY = 2.0
    WEIGHT_ACOUSTIC = 1.5
    WEIGHT_VALENCE = 1.0
    WEIGHT_DANCEABILITY = 0.5

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Compute a relevance score for one song given a UserProfile."""
        score = 0.0
        reasons = []

        # Genre match (exact)
        if song.genre.lower() == user.favorite_genre.lower():
            score += self.WEIGHT_GENRE
            reasons.append(f"matches your favorite genre ({song.genre})")

        # Mood match (exact)
        if song.mood.lower() == user.favorite_mood.lower():
            score += self.WEIGHT_MOOD
            reasons.append(f"matches your preferred mood ({song.mood})")

        # Energy proximity — penalty scales with distance
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = self.WEIGHT_ENERGY * (1.0 - energy_diff)
        score += energy_score
        if energy_diff < 0.15:
            reasons.append(f"energy level ({song.energy:.2f}) is very close to your target")

        # Acousticness preference
        if user.likes_acoustic:
            score += self.WEIGHT_ACOUSTIC * song.acousticness
            if song.acousticness > 0.7:
                reasons.append(f"highly acoustic track ({song.acousticness:.2f})")
        else:
            score += self.WEIGHT_ACOUSTIC * (1.0 - song.acousticness)
            if song.acousticness < 0.3:
                reasons.append("low acousticness matches your electric/produced taste")

        # Valence (positivity) — neutral weight
        score += self.WEIGHT_VALENCE * song.valence

        # Danceability — small bonus
        score += self.WEIGHT_DANCEABILITY * song.danceability

        # Adaptive boost: genre the user has listened to a lot
        if song.genre in user.listened_genres:
            listen_count = user.listened_genres[song.genre]
            boost = min(listen_count * 0.1, 0.5)   # cap at +0.5
            score += boost
            if boost > 0.2:
                reasons.append(f"you've been listening to a lot of {song.genre} lately")

        return round(score, 4), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked by score, best first."""
        scored = [(song, self._score_song(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def recommend_with_scores(
        self, user: UserProfile, k: int = 5
    ) -> List[Tuple[Song, float, str]]:
        """Return (song, score, explanation) tuples for display."""
        results = []
        for song in self.songs:
            score, reasons = self._score_song(user, song)
            explanation = (
                "Because: " + ", ".join(reasons) if reasons else "General fit for your taste"
            )
            results.append((song, score, explanation))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        _, reasons = self._score_song(user, song)
        if not reasons:
            return (
                f"'{song.title}' is a general fit — it shares some qualities with your taste "
                f"even though it doesn't perfectly match your top preferences."
            )
        lines = [f"'{song.title}' was recommended because it:"]
        for r in reasons:
            lines.append(f"  • {r}")
        return "\n".join(lines)

    def record_listen(self, user: UserProfile, song: Song) -> None:
        """Update the user's listen history so scores adapt over time."""
        user.listened_genres[song.genre] = user.listened_genres.get(song.genre, 0) + 1

    def record_like(self, user: UserProfile, song: Song) -> None:
        """Mark a song as liked — could be used for future collaborative filtering."""
        if song.id not in user.liked_song_ids:
            user.liked_song_ids.append(song.id)


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs.append({
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                })
    except FileNotFoundError:
        print(f"  [Warning] File not found: {csv_path}")
    print(f"  Loaded {len(songs)} songs.")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song (dict) against user preferences (dict).
    Returns (score, reasons).
    """
    score = 0.0
    reasons = []

    # Genre
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 3.0
        reasons.append(f"matches your genre ({song['genre']})")

    # Mood
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 2.5
        reasons.append(f"matches your mood ({song['mood']})")

    # Energy proximity
    target_e = float(user_prefs.get("energy", 0.5))
    energy_diff = abs(float(song.get("energy", 0.5)) - target_e)
    score += 2.0 * (1.0 - energy_diff)
    if energy_diff < 0.15:
        reasons.append(f"energy ({song['energy']:.2f}) is close to your target ({target_e:.2f})")

    # Acousticness
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acousticness = float(song.get("acousticness", 0.5))
    if likes_acoustic:
        score += 1.5 * acousticness
        if acousticness > 0.7:
            reasons.append("highly acoustic track")
    else:
        score += 1.5 * (1.0 - acousticness)

    # Valence & danceability
    score += 1.0 * float(song.get("valence", 0.5))
    score += 0.5 * float(song.get("danceability", 0.5))

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Rank all songs and return the top-k as (song_dict, score, explanation).
    """
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general fit"
        scored.append((song, s, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]