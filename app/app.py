from fastapi import FastAPI


app = FastAPI(
    title="Company Directory API",
    description="REST API для справочника организаций, зданий и видов деятельности",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Company Directory API"}

