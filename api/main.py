from fastapi import FastAPI
from api.routes import danmu, customer_service
from api.middleware import rate_limiter, auth
import uvicorn

app = FastAPI()

# 加载中间件
app.middleware("http")(rate_limiter.rate_limiter_middleware)
app.add_middleware(auth.security.__class__)

# 注册路由
app.include_router(danmu.router, prefix="/api/v1")
app.include_router(customer_service.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await RedisManager().initialize()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4
    )
