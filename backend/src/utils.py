from contextlib import asynccontextmanager

client = TGClient()

@asynccontextmanager
async def lifespan():
