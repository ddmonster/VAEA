import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from modelservice.main import Product_Introduce_NLG
from result_sample import result as fake_result
import shutil
from pathlib import Path

static_dir = Path("./frontend")


def test_in_app():
    pass


def create_app():
    app = fastapi.FastAPI()
    app.state.model = Product_Introduce_NLG()
    app.mount("/", StaticFiles(directory=static_dir.resolve()), name="static")

    @app.get("/")
    def index_page():
        return RedirectResponse("/static/index.html")

    return app


app = create_app()


def result_process(result: dict):
    img_path = Path(result["image_path"])
    shutil.copyfile(img_path, static_dir)
    result["image_path"] = f"/static/{img_path.name}"
    d1 = result.get("dashboard_1")
    d2 = result.get("dashboard_2")
    d3 = result.get("dashboard_3")
    if d1:
        shutil.copyfile(Path(d1), static_dir)
        result["dashboard_1"] = f"/static/{Path(d1).name}"
    if d2:
        shutil.copyfile(Path(d2), static_dir)
        result["dashboard_2"] = f"/static/{Path(d2).name}"
    if d3:
        shutil.copyfile(Path(d3), static_dir)
        result["dashboard_3"] = f"/static/{Path(d3).name}"
    return result


@app.post("/instruction")
def invoke_model(instruction: str):
    result: dict = app.state.model.main_run(sentence=instruction)

    return result_process(result)


@app.post("/instruction_t")
def invoke_model_test_data(instruction: str):
    return result_process(fake_result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
