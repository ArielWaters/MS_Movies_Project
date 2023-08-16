from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    print("Select storage type:")
    print("1. JSON Storage")
    print("2. CSV Storage")

    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        storage = StorageJson('movies.json')
    elif choice == 2:
        storage = StorageCsv('movies.csv')
    else:
        print("Invalid choice")
        return

    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
