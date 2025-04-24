from application import app


app.secret_key = 'tester'
if __name__ == "__main__":
    app.run(debug=False)