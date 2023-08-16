import json
import requests
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        """
        try:
            with open(self.file_path, "r") as file:
                movies_data = json.load(file)
        except FileNotFoundError:
            movies_data = {}

        return movies_data

    def add_movie(self, title, year, rating, poster):
        """
        Fetches a movie from OMDB and adds it to the movies' database.
        """
        try:
            # Make a request to the OMDb API
            url = f"http://www.omdbapi.com/?t={title}&apikey=efa33e0b"
            response = requests.get(url)
            data = response.json()

            if data["Response"] == "True":
                movie_data = {
                    "name": data["Title"],
                    "year": data["Year"],
                    "rating": data["imdbRating"],
                    "poster": data["Poster"]
                }

                movies_data = self.list_movies()
                movies_data[title] = movie_data
                self.save_movies(movies_data)
                print(f"Movie '{title}' successfully added!")
            else:
                print(f"Failed to fetch movie '{title}' from the OMDb API.")
        except requests.exceptions.RequestException:
            print("Failed to connect to the OMDb API. Please check your internet connection.")

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.
        """
        try:
            movies_data = self.list_movies()
            if title in movies_data:
                del movies_data[title]
                self.save_movies(movies_data)
                print(f"Movie '{title}' deleted successfully!")
            else:
                print(f"Movie '{title}' not found in the database.")
        except Exception as e:
            print(f"Failed to delete movie '{title}': {e}")

    def update_movie(self, title, notes):
        """
        Updates a movie from the movies' database.
        """
        try:
            movies_data = self.list_movies()
            if title in movies_data:
                movies_data[title]["notes"] = notes
                self.save_movies(movies_data)
                print(f"Notes for movie '{title}' updated.")
            else:
                print(f"Movie '{title}' not found in the database.")
        except Exception as e:
            print(f"Failed to update notes for movie '{title}': {e}")

    def save_movies(self, movies_data):
        """
        Helper function to save the movie.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump(movies_data, file, indent=4)
        except Exception as e:
            print(f"Failed to save movie(s): {e}")

    def generate_website(self):
        """
        Generates the website based on the template and movie data.
        Creates an HTML file called index.html with the full website content.
        """
        template_file = "index_template.html"
        output_file = "index.html"

        movies_data = self.list_movies()

        with open(template_file, "r") as file:
            template = file.read()

        movie_grid = ""
        for name, movie in movies_data.items():
            output = f"<div class='movie'>"
            output += f"<img class='movie-poster' src='{movie['poster']}' alt='{movie['name']}'>"
            output += f"<div class='movie-details'>"
            output += f"<div class='movie-name'>{movie['name']}</div>"
            output += f"<div class='movie-year'>{movie['year']}</div>"
            output += "</div></div>"
            movie_grid += output

        website_content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
        website_content = website_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        with open(output_file, "w") as file:
            file.write(website_content)

        print("Website was generated successfully.")


# Create an instance of StorageJson
storage = StorageJson('movies.json')
# Generate the website using the generate_website method
storage.generate_website()
