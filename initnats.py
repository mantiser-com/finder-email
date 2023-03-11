import asyncio
import nats
import os
from nats.errors import TimeoutError

async def main():
    nc = await nats.connect(os.getenv('NATS'))

    # Create JetStream context.
    js = nc.jetstream()

    # Persist messages on 'foo's subject.
    await js.add_stream(name="upload", subjects=["upload"], )
    await js.add_stream(name="result", subjects=["result","workers"] )

    # Create ordered consumer with flow control and heartbeats
    # that auto resumes on failures.
    await nc.close()




    
if __name__ == '__main__':
    asyncio.run(main())
    print("Init nats ")