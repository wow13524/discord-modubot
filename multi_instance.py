import asyncio
from modubot import Bot

def main() -> None:
    event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    event_loop.create_task(Bot(config_name="example_configs/configA.json").start())
    event_loop.create_task(Bot(config_name="example_configs/configB.json").start())

    event_loop.run_forever()

if __name__ == "__main__":
    main()