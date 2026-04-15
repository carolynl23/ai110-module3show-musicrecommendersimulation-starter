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

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
