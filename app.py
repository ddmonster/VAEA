import fastapi

def create_app():
    app = fastapi.FastAPI()

    app.mount("./frontend",app,"/")

    app.