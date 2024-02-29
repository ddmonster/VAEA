import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from modelservice.main import Product_Introduce_NLG
from result_sample import result as fake_result
import shutil
from pathlib import Path
from pydantic  import BaseModel
file_path = Path(__file__).parent.resolve()
static_dir = file_path.joinpath("frontend")
chart_dir = file_path.joinpath("modelservice").joinpath("chart").joinpath("chart_html")
img_dir = file_path.joinpath("modelservice").joinpath("database").joinpath("images")
def test_in_app():
    pass


app = fastapi.FastAPI()
app.state.model = Product_Introduce_NLG()
app.mount("/static", StaticFiles(directory=static_dir.resolve()), name="static")
app.mount("/chart", StaticFiles(directory=chart_dir.resolve()), name="chart")
app.mount("/img", StaticFiles(directory=img_dir.resolve()), name="img")
@app.get("/")
async def index_page():
    return RedirectResponse("/static/index.html")
def result_process(result: dict):
    img_path = Path(result["image_path"])
    result["image_path"] = f"/img/{img_path.name}"
    d1 = result.get("dashboard_1")
    d2 = result.get("dashboard_2")
    d3 = result.get("dashboard_3")
    if d1:
        result["dashboard_1"] = f"/chart/{Path(d1['html_path']).name}"
    if d2:
        result["dashboard_2"] = f"/chart/{Path(d2['html_path']).name}"
    if d3:
        result["dashboard_3"] = f"/chart/{Path(d3['html_path']).name}"
    return result
class Instruction(BaseModel):
        instruction: str
@app.post("/instruction/")
async def invoke_model(instruction:Instruction):
    print(instruction)
    result: dict = app.state.model.main_run(sentence=instruction)
    print(result)
    return result_process(result)


@app.get("/instruction_t/")
async def invoke_model_test_data():
    return result_process(fake_result)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app,host="127.0.0.1",port=8899)
