#!/usr/bin/env python

import asyncio
from game import Othello
import json

from websockets.asyncio.server import serve

connections = {}

async def handler(websocket):
    # # parse the connection url
    # if not websocket.request.path.startswith('/ws/server/'):
    #     return
    # deconstructed_url = websocket.request.path.split('/')
    # if len(deconstructed_url) != 5:
    #     return 
    # match_id = deconstructed_url[3]
    # 
    # path = websocket.request.path
    # print(path)
    game = Othello()
    await websocket.send(json.dumps({
        'grid': game.grid,
        'team': 1,
        'move': game.move
    }))
    async for message in websocket:
        print(message)
        resp = game.make_move(1, 4, 5)
        print(resp['message'])
        print("successfully made move")
        print(game.grid)
        await websocket.send(json.dumps(game.grid))
    
async def main():
    async with serve(handler, "localhost", 8001):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())