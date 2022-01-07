import pandas as pd
pd.pandas.set_option('display.max_columns', 20)
pd.set_option('display.expand_frame_repr', False)

#############################################
# Veri Hazırlama işlemlerini gerçekleştiriniz.
#############################################

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

#############################################
# Öneri yapılacak kullanıcının izlediği filmleri belirleyiniz.
#############################################

random_user = 108170

random_user_df = user_movie_df[user_movie_df.index == random_user]
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

#############################################
# Aynı filmleri izleyen diğer kullanıcıların verisine ve Id'lerine erişiniz.
#############################################

movies_watched_df = user_movie_df[movies_watched]

user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.sort_values("movie_count", ascending=True)

perc = len(movies_watched) * 60 // 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

#############################################
# Öneri yapılacak kullanıcı ile en benzer kullanıcıları belirleyiniz.
#############################################

final_df = movies_watched_df[movies_watched_df.index.isin(users_same_movies)]

corr_df = final_df.T.corr().unstack().sort_values()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()

top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)

top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')

top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')

top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]

#############################################
# Weighted Average Recommendation Score'u hesaplayınız ve ilk 5 filmi tutunuz.
#############################################

top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()
recommendation_df[recommendation_df["weighted_rating"] > 3.5]

movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating",
                                                                                                 ascending=False)[0:5]

#############################################
# Kullanıcının izlediği filmlerden en son en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
#############################################
#: 5 öneri user-based
#: 5 öneri item-based
#: olacak şekilde 10 öneri yapınız.
#: Not: Çıktılarınız farklılık gösterebilir.


user = 108170
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')

movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)]. \
               sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]


def item_based_recommender(movie_name, user_movie_df):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)


movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df)

movies_from_item_based[1:11].index

