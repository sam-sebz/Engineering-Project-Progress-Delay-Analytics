import asyncio,httpx
from src.main import app
from src.db import init_db
init_db()
async def main():
    transport=httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport,base_url="http://test") as c:
        assert (await c.get("/api/health")).status_code==200
        r=await c.get("/api/projects")
        assert r.status_code==200 and len(r.json())>0
        q=await c.post("/api/projects",json={"name":"Smoke Project","budget":100000})
        assert q.status_code==200
    print("P3 smoke tests passed")
asyncio.run(main())