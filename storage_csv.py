import csv
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        """
        movies_data = {}
        try:
            with open(self.file_path, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    movie_data = {
                        "name": row["name"],
                        "year": row["year"],
                        "rating": row["rating"],
                        "poster": row["poster"]
                    }
                    movies_data[row["name"]] = movie_data
        except FileNotFoundError:
            pass
        return movies_data

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the movies' database.
        """
        movies_data = self.list_movies()
        if title not in movies_data:
            with open(self.file_path, "a", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([title, year, rating, poster])

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.
        """
        movies_data = self.list_movies()
        if title in movies_data:
            new_movies = [movie for movie in movies_data if movie != title]
            with open(self.file_path, "w", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["name", "year", "rating", "poster"])
                for movie in new_movies:
                    movie_data = movies_data[movie]
                    csv_writer.writerow([movie, movie_data["year"], movie_data["rating"], movie_data["poster"]])

    def update_movie(self, title, notes):
        """
        Updates a movie from the movies' database.
        """
        movies_data = self.list_movies()
        if title in movies_data:
            movies_data[title]["notes"] = notes
            with open(self.file_path, "w", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["name", "year", "notes", "poster"])
                for movie, movie_data in movies_data.items():
                    csv_writer.writerow([movie, movie_data["year"], movie_data["notes"], movie_data["poster"]])

    def save_movies(self, movies_data):
        """
        Helper function to save the movie.
        """
        with open(self.file_path, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["name", "year", "rating", "poster"])
            for movie, movie_data in movies_data.items():
                csv_writer.writerow([movie, movie_data["year"], movie_data["rating"], movie_data["poster"]])

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
