    # importing spacy and loading medium ("en_core_web_md") module
    import spacy
    nlp = spacy.load("en_core_web_md")

    # The following function is based on one parameter - previously watched movie description
    # which is then  to be compared against potential recommendations for similarity.
    # It displays all potential recommendation titles along with similarity score
    # and then prints out statement which movie had the highest similarity score that viewer is most likely to watch based on the description.

    def most_likely_movie (description_to_compare):
        watched_nlp = nlp(description_to_compare)
        max_similarity = -1
        position = 0
        for i, movie in enumerate(movie_descriptions):
            movie_nlp = nlp(movie)
            print(f" {movie_titles[i]}:\t{movie_nlp.similarity(watched_nlp)}")
            if (movie_nlp.similarity(watched_nlp)) > max_similarity:
                max_similarity = (movie_nlp.similarity(watched_nlp))
                position = i
        print(
            f"\nThe viewer is most likely to watch '{movie_titles[position]}' because description has {max_similarity} similarity to the one viewer previously watched.")


    prev_watched_title = ("Planet Hulk")
    prev_watched_description = ("""Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, 
    the Illuminati trick Hulk into a shuttle and launch him into space to a planet Sakaar where he is sold to slavery and trained as a gladiator.""")

    # The following reads from file and splits data to two lists: 'movie_titles' and 'movie_descriptions'
    try:
        file = open("movies.txt", "r", encoding = "utf-8-sig")
        file_content = file.readlines()
        movie_titles = []
        movie_descriptions = []
        for line in file_content:
            split_line = line.strip("\n").split(" :")
            movie_titles.append(split_line[0])
            movie_descriptions.append(split_line[1])

        # Calling function to return similarities along with movie title with max_similarity
        most_likely_movie(prev_watched_description)

    except FileNotFoundError:
        print("Error: File not found. Please double check that file is in correct directory and try again.")
