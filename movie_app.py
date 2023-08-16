import random
import requests
from storage_json import StorageJson


class MovieApp:
    def __init__(self, storage):
        """
        Initializes the MovieApp with a storage instance.
        Args:
            storage (IStorage): An instance of a storage class implementing the IStorage interface.
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        Lists all the movies in the database.
        """
        movies = self._storage.list_movies()
        for name, movie in movies.items():
            print(f"{name}: {movie['rating']}, {movie['year']}")

    def _command_add_movie(self):
        """
        Fetches a movie from OMDB and adds it to the movies' database.
        """
        title = input("Enter movie title: ")

        # Fetch movie information from the OMDB API
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey=efa33e0b"
            response = requests.get(url)
            data = response.json()

            if data["Response"] == "True":
                year = data["Year"]
                rating = data["imdbRating"]
                poster = data["Poster"]

                # Call the add_movie method in the StorageJson object to add the movie
                self._storage.add_movie(title, year, rating, poster)
                print(f"Movie '{title}' successfully added!")
            else:
                print(f"Failed to fetch movie '{title}' from the OMDb API.")
        except requests.exceptions.RequestException:
            print("Failed to connect to the OMDb API. Please check your internet connection.")

    def _command_movie_stats(self):
        """
        Displays statistics for the movies in the database.
        """
        movies_data = self._storage.list_movies()
        ratings = [float(movie['rating']) for movie in movies_data.values()]

        avg_rating = sum(ratings) / len(ratings)
        print(f"Average rating: {avg_rating:.2f}")

        n = len(ratings)
        sorted_ratings = sorted(ratings)
        if n % 2 == 0:
            median_rating = (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
        else:
            median_rating = sorted_ratings[n // 2]
        print(f"Median rating: {median_rating:.2f}")

        best_movies = [name for name, movie in movies_data.items() if movie['rating'] == max(ratings)]
        for movie in best_movies:
            print(f"Best movie: {movie}, {movies_data[movie]['rating']}")

        worst_movies = [name for name, movie in movies_data.items() if movie['rating'] == min(ratings)]
        for movie in worst_movies:
            print(f"Worst movie: {movie}, {movies_data[movie]['rating']}")

    def _command_random_movie(self):
        """
        Selects a random movie from the list and prints its name and rating.
        """
        movies_data = self._storage.list_movies()
        random_movie_name = random.choice(list(movies_data.keys()))
        random_movie = movies_data[random_movie_name]
        print(f"Your movie for tonight: {random_movie_name}. It's rated {random_movie['rating']}.")

    def _command_search_movie(self):
        """
        Searches for movies based on a partial name entered by the user.
        """
        user_input = input("Enter part of movie name: ").lower()
        movies_data = self._storage.list_movies()
        found_movies = []
        for name, movie in movies_data.items():
            if user_input in name.lower():
                found_movies.append(f"{name}, {movie['rating']}")
        if found_movies:
            print("\n".join(found_movies))
        else:
            print("No movies found")

    def _command_sorted_movies(self):
        """
        Sorts and displays the movies in descending order of their ratings.
        """
        movies_data = self._storage.list_movies()
        sorted_movies_data = sorted(movies_data.items(), key=lambda x: float(x[1]['rating']), reverse=True)

        for name, movie in sorted_movies_data:
            print(f"{name}, {movie['rating']}")

    def _generate_website(self):
        """
        Generates a website based on the movies in the database.
        """
        self._storage.generate_website()

    def run(self):
        """
        Runs the MovieApp, presenting the user with a menu and handling user inputs.
        """
        while True:
            print("******** My Movies Database ********")
            print("Menu:")

            menu_movies = {
                "0.": "Exit",
                "1.": "List movies",
                "2.": "Add movie",
                "3.": "Delete movie",
                "4.": "Update movie",
                "5.": "Stats",
                "6.": "Random movie",
                "7.": "Search movie",
                "8.": "Movies sorted by rating",
                "9.": "Generate website"
            }

            for key, value in menu_movies.items():
                print(key, value)

            print()
            user_input = int(input("Enter choice (0-8): "))
            if user_input == 0:
                print("Bye!")
                break
            elif user_input == 1:
                self._command_list_movies()
                print()
            elif user_input == 2:
                self._command_add_movie()
                print()
            elif user_input == 3:
                title = input("Enter movie title to delete: ")
                self._storage.delete_movie(title)
                print()
            elif user_input == 4:
                title = input("Enter movie title: ")
                notes = input("Enter new movie notes: ")
                self._storage.update_movie(title, notes)
                print()
            elif user_input == 5:
                self._command_movie_stats()
                print()
            elif user_input == 6:
                self._command_random_movie()
                print()
            elif user_input == 7:
                self._command_search_movie()
                print()
            elif user_input == 8:
                self._command_sorted_movies()
                print()
            elif user_input == 9:
                self._generate_website()
                print()

            ending = input("Press enter to continue")


if __name__ == "__main__":
    storage = StorageJson('movies.json')  # Instantiate the storage class
    app = MovieApp(storage)
    app.run()
