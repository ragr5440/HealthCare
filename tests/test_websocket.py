import asyncio
import json

import websockets


async def test_chat() -> None:
    uri = "ws://127.0.0.1:8000/chat"

    async with websockets.connect(
        uri
    ) as websocket:
        message = (
            "Check appointment status for APT-0015"
        )

        print(
            "Sending:",
            message,
        )

        await websocket.send(
            message
        )

        response = await websocket.recv()

        print("\nReceived:")

        try:
            parsed_response = json.loads(
                response
            )

            print(
                json.dumps(
                    parsed_response,
                    indent=2,
                    ensure_ascii=False,
                )
            )

        except json.JSONDecodeError:
            print(response)


if __name__ == "__main__":
    asyncio.run(
        test_chat()
    )