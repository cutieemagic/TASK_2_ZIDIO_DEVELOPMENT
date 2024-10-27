# Sample movie dataset
movies = [
    {'movie_id': 1, 'title': 'Toy Story', 'genres': 'Animation|Children\'s|Comedy'},
    {'movie_id': 2, 'title': 'Jumanji', 'genres': 'Adventure|Children\'s|Fantasy'},
    {'movie_id': 3, 'title': 'Grumpier Old Men', 'genres': 'Comedy|Romance'},
    {'movie_id': 4, 'title': 'Waiting to Exhale', 'genres': 'Comedy|Drama|Romance'},
    {'movie_id': 5, 'title': 'Father of the Bride', 'genres': 'Comedy'}
]

# Sample user ratings
ratings = [
    {'user_id': 1, 'movie_id': 1, 'rating': 5},
    {'user_id': 1, 'movie_id': 2, 'rating': 3},
    {'user_id': 2, 'movie_id': 2, 'rating': 4},
    {'user_id': 2, 'movie_id': 3, 'rating': 2},
    {'user_id': 3, 'movie_id': 4, 'rating': 5},
    {'user_id': 3, 'movie_id': 5, 'rating': 3}
]
# Helper function to get ratings by a specific user
def get_user_ratings(user_id):
    return [r for r in ratings if r['user_id'] == user_id]

# Helper function to calculate similarity between two users based on common ratings
def calculate_similarity(user1_ratings, user2_ratings):
    common_ratings = []
    for r1 in user1_ratings:
        for r2 in user2_ratings:
            if r1['movie_id'] == r2['movie_id']:
                common_ratings.append((r1['rating'], r2['rating']))
    
    if not common_ratings:
        return 0  # No common ratings
    
    # Use Pearson Correlation coefficient to calculate similarity
    n = len(common_ratings)
    sum1 = sum([r1 for r1, r2 in common_ratings])
    sum2 = sum([r2 for r1, r2 in common_ratings])
    
    sum1Sq = sum([r1 ** 2 for r1, r2 in common_ratings])
    sum2Sq = sum([r2 ** 2 for r1, r2 in common_ratings])
    
    pSum = sum([r1 * r2 for r1, r2 in common_ratings])
    
    num = pSum - (sum1 * sum2 / n)
    den = ((sum1Sq - sum1 ** 2 / n) * (sum2Sq - sum2 ** 2 / n)) ** 0.5
    if den == 0:
        return 0
    
    return num / den

# Function to get movie recommendations for a user based on collaborative filtering
def collaborative_filtering_recommend(user_id):
    user_ratings = get_user_ratings(user_id)
    
    # Find other users and their similarity score with the given user
    other_users = set([r['user_id'] for r in ratings]) - {user_id}
    similarities = []
    for other_user in other_users:
        other_user_ratings = get_user_ratings(other_user)
        sim = calculate_similarity(user_ratings, other_user_ratings)
        similarities.append((other_user, sim))
    
    # Sort users by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Recommend movies based on the ratings of the most similar user
    most_similar_user = similarities[0][0]
    most_similar_user_ratings = get_user_ratings(most_similar_user)
    
    # Recommend movies that the current user hasn't rated yet
    recommended_movies = []
    for rating in most_similar_user_ratings:
        if not any(r['movie_id'] == rating['movie_id'] for r in user_ratings):
            recommended_movies.append(rating['movie_id'])
    
    return [movie for movie in movies if movie['movie_id'] in recommended_movies]

# Test collaborative filtering recommendations for user 1
print("Collaborative Filtering Recommendations for User 1:")
print(collaborative_filtering_recommend(1))
# Helper function to compute genre similarity using Jaccard similarity
def genre_similarity(movie_genres_1, movie_genres_2):
    genres_1 = set(movie_genres_1.split('|'))
    genres_2 = set(movie_genres_2.split('|'))
    intersection = genres_1.intersection(genres_2)
    union = genres_1.union(genres_2)
    return len(intersection) / len(union) if union else 0

# Function to get content-based recommendations
def content_based_recommend(movie_title, n_recommendations=5):
    movie = next((m for m in movies if m['title'] == movie_title), None)
    if not movie:
        return []
    
    # Calculate similarity scores with other movies
    similarities = []
    for other_movie in movies:
        if other_movie['movie_id'] != movie['movie_id']:
            sim = genre_similarity(movie['genres'], other_movie['genres'])
            similarities.append((other_movie['title'], sim))
    
    # Sort movies by similarity and return top N recommendations
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:n_recommendations]

# Test content-based recommendations for "Toy Story"
print("Content-Based Recommendations for 'Toy Story':")
print(content_based_recommend('Toy Story'))

# Hybrid recommendation combining collaborative filtering and content-based filtering
def hybrid_recommendation(user_id, movie_title):
    # Get recommendations from collaborative filtering
    collab_recommendations = collaborative_filtering_recommend(user_id)
    collab_titles = [movie['title'] for movie in collab_recommendations]
    
    # Get recommendations from content-based filtering
    content_recommendations = content_based_recommend(movie_title)
    content_titles = [title for title, _ in content_recommendations]
    
    # Combine and remove duplicates
    combined_recommendations = list(set(collab_titles + content_titles))
    return combined_recommendations

# Test hybrid recommendations for user 1 and "Toy Story"
print("Hybrid Recommendations for User 1 and 'Toy Story':")
print(hybrid_recommendation(1, 'Toy Story'))
