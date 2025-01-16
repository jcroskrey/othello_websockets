#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve

async def handler(websocket):
    async for message in websocket:
        print(message)
    
async def main():
    async with serve(handler, "localhost", 8001):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())