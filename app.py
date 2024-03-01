import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from result_sample import result as fake_result
from pathlib import Path
from pydantic import BaseModel
import re

file_path = Path(__file__).parent.resolve()
static_dir = file_path.joinpath("frontend")
chart_dir = file_path.joinpath("modelservice").joinpath("chart").joinpath("chart_html")
img_dir = file_path.joinpath("modelservice").joinpath("database").joinpath("images")


def test_in_app():
    pass


app = fastapi.FastAPI()
# app.state.model = Product_Introduce_NLG()
app.mount("/static", StaticFiles(directory=static_dir.resolve()), name="static")
app.mount("/chart", StaticFiles(directory=chart_dir.resolve()), name="chart")
app.mount("/img", StaticFiles(directory=img_dir.resolve()), name="img")


@app.get("/")
async def index_page():
    return RedirectResponse("/static/index.html")


def result_process(result: dict):
    get_name = lambda x: x.split("\\")[-1]
    m = re.search("[0-1A-Za-z].*", result["product_introduction"])
    result["product_introduction"]
    img_path = get_name(result["image_path"])
    result["image_path"] = f"/img/{img_path}"
    d1 = result.get("dashboard_1")
    d2 = result.get("dashboard_2")
    d3 = result.get("dashboard_3")
    if d1:
        name = get_name(d1["html_path"])
        result["dashboard_1"]["html_path"] = f"/chart/{name}"
    if d2:
        name = get_name(d2["html_path"])
        result["dashboard_2"]["html_path"] = f"/chart/{name}"
    if d3:
        name = get_name(d3["html_path"])
        result["dashboard_3"]["html_path"] = f"/chart/{name}"
    return result


class Instruction(BaseModel):
    instruction: str


@app.post("/instruction/")
async def invoke_model(instruction: Instruction):
    from modelservice.main import Product_Introduce_NLG

    instance = Product_Introduce_NLG()
    print(instruction)
    result: dict = instance.main_run(sentence=instruction)
    print(result)
    return result_process(result)


from copy import deepcopy


@app.post("/instruction_t/")
async def invoke_model_test_data(instruction: Instruction):
    rest = deepcopy(fake_result)
    return result_process(rest)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8899)
