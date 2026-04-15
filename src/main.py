"""
Command line runner for the Music Recommender Simulation.
"""

from recommender import load_songs, recommend_songs
from recommender import Song, UserProfile, Recommender


def print_header():
    print("\n" + "=" * 55)
    print("  🎵  Music Recommender Simulation")
    print("=" * 55)


def demo_functional_api(songs_path: str = "data/songs.csv"):
    """Demo using the simple dict-based functional API."""
    songs = load_songs(songs_path)

    profiles = [
        {"name": "Pop / Happy / High Energy", "genre": "pop",   "mood": "happy",  "energy": 0.85, "likes_acoustic": False},
        {"name": "Lofi / Chill / Low Energy",  "genre": "lofi",  "mood": "chill",  "energy": 0.40, "likes_acoustic": True},
        {"name": "Rock / Intense listener",    "genre": "rock",  "mood": "intense","energy": 0.90, "likes_acoustic": False},
    ]

    for profile in profiles:
        name = profile.pop("name")
        print(f"\n{'─'*55}")
        print(f"  User: {name}")
        print(f"{'─'*55}")
        recs = recommend_songs(profile, songs, k=3)
        for i, (song, score, explanation) in enumerate(recs, 1):
            print(f"  {i}. {song['title']} — {song['artist']}")
            print(f"     Score: {score:.2f}  |  {explanation}")
        profile["name"] = name   # restore for display


def demo_oop_api():
    """Demo using the OOP Recommender with adaptive listening."""
    print(f"\n{'─'*55}")
    print("  OOP API — Adaptive Listener Demo")
    print(f"{'─'*55}")

    import csv, os
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, "..", "data", "songs.csv")
    songs_dicts = load_songs(csv_path)
    songs = [
        Song(
            id=s["id"], title=s["title"], artist=s["artist"],
            genre=s["genre"], mood=s["mood"], energy=s["energy"],
            tempo_bpm=s["tempo_bpm"], valence=s["valence"],
            danceability=s["danceability"], acousticness=s["acousticness"],
        )
        for s in songs_dicts
    ]

    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    rec = Recommender(songs)

    print("\n  [Before listening history]")
    results = rec.recommend_with_scores(user, k=3)
    for song, score, expl in results:
        print(f"  • {song.title} ({song.genre})  Score: {score:.2f}")
        print(f"    {expl}")

    # Simulate the user listening to lofi tracks repeatedly
    lofi_songs = [s for s in songs if s.genre == "lofi"]
    for s in lofi_songs * 3:   # listen 3x each
        rec.record_listen(user, s)

    print("\n  [After listening to lots of lofi]")
    results = rec.recommend_with_scores(user, k=3)
    for song, score, expl in results:
        print(f"  • {song.title} ({song.genre})  Score: {score:.2f}")
        print(f"    {expl}")


def main() -> None:
    print_header()
    demo_functional_api("data/songs.csv")
    demo_oop_api()
    print("\n" + "=" * 55 + "\n")


if __name__ == "__main__":
    main()