import inotify.adapters
import inotify.constants
import pathlib
import threading
import queue


def listen(q: queue.Queue):
    i = inotify.adapters.Inotify()

    parent = pathlib.Path(".")
    events = (
        inotify.constants.IN_CREATE
        | inotify.constants.IN_MOVED_FROM
        | inotify.constants.IN_MOVED_TO
        | inotify.constants.IN_MODIFY
        | inotify.constants.IN_CLOSE_WRITE
        | inotify.constants.IN_DELETE
    )

    for subdir in [
        parent / "layouts",
        parent / "assets",
        parent / "content",
        parent / "static",
    ]:
        for dir in subdir.rglob("**"):
            i.add_watch(str(dir), mask=events)

    i.add_watch(str(parent / "config.toml"), mask=events)

    for event in i.event_gen(yield_nones=False):
        assert event is not None
        (_, type_names, path, filename) = event
        if "IN_ISDIR" in type_names:
            if "IN_CREATE" in type_names or "IN_MOVED_TO" in type_names:
                i.add_watch(str(parent / path / filename), mask=events)
            elif "IN_MOVED_FROM" in type_names or "IN_DELETE" in type_names:
                i.remove_watch(str(parent / path / filename))
        q.put(str(parent / path / filename))


def main():
    q = queue.Queue()
    t = threading.Thread(target=listen, args=(q,), daemon=True).start()

    cache = set()
    while True:
        try:
            event = q.get(timeout=0.2)
        except queue.Empty:
            if cache:
                print(cache, flush=True)
                cache.clear()
        else:
            cache.add(event)
            q.task_done()


if __name__ == "__main__":
    main()
