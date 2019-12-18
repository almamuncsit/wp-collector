from application import app


def job():
    print("I'm working...")


if __name__ == "__main__":
    app.run(debug=True)
