import fastapi
import fastapi.middleware.cors
import pydantic

from seo_analyzer import analyse_website


app = fastapi.FastAPI(
    title="AI-Powered SEO Audit API",
    description="Analyse one webpage and return technical SEO results.",
    version="1.0.0",
)


# Allow your local frontend to communicate with the backend.
# We will add your deployed frontend origin when we deploy the API.
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class AuditRequest(pydantic.BaseModel):
    url: str = pydantic.Field(
        min_length=8,
        max_length=2048,
        description="The full URL of the webpage to analyse.",
    )


@app.get("/")
def home():
    return {
        "message": "SEO Audit API is running.",
        "documentation": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SEO Audit API",
    }


@app.post("/api/analyze")
def analyze_page(request: AuditRequest):

    try:
        results = analyse_website(request.url)
        return results

    except ValueError as error:
        raise fastapi.HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise fastapi.HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analysing this webpage.",
        )

   
