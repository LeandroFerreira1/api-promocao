from fastapi import FastAPI

from api_promo.core.configs import settings
from api_promo.api.api import api_router


app = FastAPI(title='API - PROMO')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
