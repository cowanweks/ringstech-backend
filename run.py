from app import create_app


flask_app = create_app()


def main():
    flask_app.run(host=flask_app.config.get("HOST"), port=flask_app.config.get("PORT"))


if __name__ == "__main__":
    main()
