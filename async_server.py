import asyncio
import json


HOST = "localhost"
PORT = 12000


player_positions = {"1": {"x": 100, "y": 100}, "2": {"x": 200, "y": 200}}


async def handler(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("data to client closed")
                break
            player_pos = data.decode()
            player_pos = json.loads(player_pos)
            player_id = player_pos["player_id"]

            if player_id == "1":
                send_id = "2"
            else:
                send_id = "1"

            # update the players position
            player_positions[player_id]["x"] = player_pos["x"]
            player_positions[player_id]["y"] = player_pos["y"]

            # send the client the position of the opposition
            response_position = player_positions[send_id]
            message = json.dumps(response_position).encode('utf-8')

            # echo back to client
            writer.write(message)
            await writer.drain()

    except Exception as e:
        print("Error", e)

    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handler, HOST, PORT)
    # report on our server
    print("Server details ", server)
    print(f"Serving {server.is_serving()}")

    # accept connections until the connection is closed
    await server.serve_forever()

    print(f"Serving {server.is_serving()}")


if __name__ == "__main__":
    asyncio.run(main())
