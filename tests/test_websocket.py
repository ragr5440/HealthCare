import asyncio
import websockets


async def test_chat():

    uri = "ws://127.0.0.1:8000/chat"

    async with websockets.connect(uri) as websocket:

        await websocket.send("Appointment Status")

        response = await websocket.recv()

        print(response)

        await websocket.close()


asyncio.run(test_chat())