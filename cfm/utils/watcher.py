import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cfm.engine.transformer import apply_rules
from cfm.utils.ruleloader import resolve_rule_path

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, lang, ruleset):
        self.lang = lang
        self.rules_path = resolve_rule_path(ruleset, lang)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".cpp"):
            print(f"🔁 Re-fixing: {event.src_path}")
            apply_rules([event.src_path], self.rules_path)

def watch_directory(path, lang, ruleset):
    observer = Observer()
    observer.schedule(ChangeHandler(lang, ruleset), path, recursive=True)
    observer.start()
    print(f"👀 Watching {path} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
