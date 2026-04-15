# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name: SongPlay

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

- SongPlay suggests songs from a small catalog based on a user's preferred genre,mood, target energy level, and acoustic preference. It is designed for classroom exploration of how content-based recommender systems work, not for production use with real users. The system also includes a lightweight adaptive component that boosts genres the user has listened to recently, simulating how a real app might learn from listening history.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- Every song in the catalog has six numerical or categorical attributes: genre, mood,energy (0–1), tempo, acousticness (0–1), valence (emotional positivity, 0–1), and danceability (0–1).
- Every user has four preference values: a favorite genre, a favorite mood, a target energy level, and a yes/no flag for whether they like acoustic music.
- To score a song, the model checks each preference against the song's attributes and awards points using fixed weights:

    - Genre match is worth the most (3.0 points) because genre is the strongest signal of taste.
    - Mood match is worth slightly less (2.5 points) because mood can vary by context even within a favorite genre. 
    - Energy proximity contributes up to 2.0 points — songs whose energy is closest to the user's target score highest; the penalty grows the further away the energy is.
    - Acousticness contributes up to 1.5 points depending on whether the user prefers acoustic or electric/produced sounds.
    - Valence and danceability add small bonuses (1.0 and 0.5 respectively) to break ties in favor of positive, danceable tracks.

- After all weights are summed, the songs are ranked from highest to lowest score and the top-k are returned as recommendations. An adaptive component adds a small bonus (capped at 0.5) for genres the user has been listening to frequently, letting the profile drift toward recent listening patterns over time.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

- the catalog contains 20 songs stored in data/songs.csv. The dataset covers seven genres: pop, lofi, rock, synthwave, ambient, jazz, indie pop, and acoustic.  Moods represented include happy, chill, intense, moody, relaxed, focused, and to a lesser extent neutral. 
- The catalog was written by hand to illustrate a range of feature combinations. It skews toward pop and lofi (the two largest genre groups) and toward English-language
- Western popular music. Genres like classical, hip-hop, R&B, country, and non-Western music traditions are entirely absent. The data mostly reflects tastes familiar to a North American or European pop/indie listener.
- No songs were removed from the starter set; 10 additional songs were added to give the recommender more to work with and to create a second song for each genre.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- Transparent: Every score is the sum of weighted, human-readable rules. There are no hidden layers or black-box transformations.
- Genre-first users are well served: For a pop fan who wants happy, high-energy tracks the system reliably surfaces the right songs from the catalog.
- Acoustic vs electric preference is captured explicitly, which is a meaningful dimension that many simple recommenders overlook.
- Adaptive listening history lets the profile change over time without requiring a full retraining step, just a counter increment.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- Cold start for non-pop/lofi users: Rock, jazz, ambient, and synthwave each have only two catalog entries. A rock fan will see the same two songs recommended repeatedly.
- Genre over-dominance: Because genre carries the highest weight (3.0), a user whose favorite genre doesn't match anything in the catalog gets weaker recommendations than deserved.
- No cross-genre discovery: The system will never recommend a jazz song to a pop fan even if the song has very similar energy and valence. Real listeners often enjoy songs outside their stated genre.
- Mood is binary: Mood matching is all-or-nothing. A user who likes "happy" gets nothing for "relaxed" even though these are acoustically similar.
- Demographic gap: The catalog reflects a narrow slice of music culture. A user whose tastes center on hip-hop, K-pop, cumbia, or any unlisted genre effectively gets random recommendations.
- Filter bubble risk: The adaptive boost reinforces whatever genre the user already listens to most, reducing exposure to new sounds over time.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

- three user profiles were tested manually:
    - pop/happy, lofi/chill, rock/intense
- the tests confirmed that after similating 6 listens to lofi tracks, the lofi score for a nominally-pop user increased from 2.67 to 2.70, a small but correct directional shift 
- automated tests: correct ranking order, k-limiting behavior, exmplanation non-emptiness, genre mention in explanations, adaptive score increase after listening

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- Soft genre similarity: Instead of exact genre matching, use a genre similarity matrix so that "indie pop" scores partially for a "pop" user.
- Mood proximity: Encode mood as a vector (e.g., arousal/valence axes from music psychology) so "happy" and "relaxed" are close while "intense" and "chill" are far.
- Diversity injection: After ranking by score, swap one or two of the top-k results for songs from underrepresented genres to fight filter bubbles.
- Collaborative filtering layer: Track which songs users with similar profiles liked and incorporate those signals alongside content features.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- Building SongPlay made the abstract idea of a "recommendation algorithm" concrete and surprisingly humbling. Even with only six features and twenty songs, it was easy to accidentally design a system that worked perfectly for pop fans and poorly for everyone else just because pop was the most represented genre in the catalog. That made it very clear how bias in training data and catalog composition can quietly shape who a system serves well, even when the math itself is fair.
- The most surprising moment was realizing that the weighted-sum approach never discovers anything genuinely new for the user. A pop fan will always get pop because genre carries the most weight and there is no mechanism to reward novelty or serendipity. Real recommenders like Spotify's Discover Weekly clearly solve this probably by measuring "how different is this song from what you usually hear" as a positive signal, not a penalty. That realization changed how I think about recommendation as a design problem: the goal isn't to find the best match, it's to find the best mix of familiarity and surprise.