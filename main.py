import uvicorn

from src.application import create_app
from prometheus_fastapi_instrumentator import Instrumentator

app = create_app()

instrumentator = Instrumentator().instrument(app)
@app.on_event("startup")
async def _startup():
    instrumentator.expose(app, endpoint='/metrics', tags=['metrics'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
