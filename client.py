#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect


async def hello():
    async with connect("ws://localhost:8001") as websocket:
        message = await websocket.recv()
        await websocket.send("Hello world!")
        print(message)


if __name__ == "__main__":
    asyncio.run(hello())