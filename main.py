import aioredis 
from fastapi import FastAPI, Request, Query 

app = FastAPI() 
async def get_redis_pool() -> aioredis.Redis: 
		redis = aioredis.from_url(
        		"redis://localhost", encoding="utf-8", decode_responses=True
    	)
		return redis 

@app.on_event('startup') 
async def startup_event(): 
		app.state.redis = await get_redis_pool() 

@app.on_event('shutdown') 
async def shutdown_event(): 
		app.state.redis.close() 
		await app.state.redis.wait_closed() 

@app.get("/test", summary="测试redis") 
async def test_redis(request: Request, num: int=Query(123, title="参数num")):
	 await request.app.state.redis.set("aa", num)
	 v = await request.app.state.redis.get("aa")
	 print(v, type(v))
	 return {"msg": v}

@app.get("/test_hash", summary="测试redis") 
async def test_redis(request: Request, num: int=Query(123, title="参数num")):
	 await request.app.state.redis.hmset('hash',{'name': 'Jerry', 'species': 'mouse'})
	 v = await request.app.state.redis.hgetall('hash')
	 print(v, type(v))
	 return {"msg": v}

	 

if __name__ == '__main__':
	import uvicorn
	uvicorn.run(app='main:app', host="127.0.0.1", port=8080, reload=True, debug=True)
