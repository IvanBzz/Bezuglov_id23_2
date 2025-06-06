import asyncio
import websockets
import json
import sys
import requests


async def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py f.rar")
        return

    file_path = sys.argv[1]

    # Запуск задачи через REST API
    response = requests.post(
        "http://localhost:8000/crack/",
        json={"file_path": file_path}
    )

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return

    task_data = response.json()
    task_id = task_data["task_id"]
    ws_url = f"ws://localhost:8000/ws/{task_id}"

    print(f"Task started. ID: {task_id}")
    print("Listening for updates...")

    # Подключение к WebSocket
    async with websockets.connect(ws_url) as websocket:
        while True:
            message = await websocket.recv()
            event = json.loads(message)

            status = event["status"]
            if status == "hash_extracted":
                print("\n[+] Hash extracted successfully")
            elif status == "success":
                print(f"\n[+] Password found: {event['password']}")
                break
            elif status in ["failure", "error"]:
                print(f"\n[-] {event['message']}")
                break
            else:
                print(f"\n[!] Unknown status: {status}")
                break


if __name__ == "__main__":
    asyncio.run(main())