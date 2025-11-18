import tornado.queues


async def process_tornado_queue(q: tornado.queues.Queue):

    if q.empty():
        raise ValueError("Error: Queue must be pre-populated with non-primitive data")
    item = await q.get()
    try:

        return item.process()
    except AttributeError:
        raise ValueError("Error: Queue item does not have a process() method")