from .ui.app import AutomationHub
from .core.headless import run_headless_organizer, run_headless_cleaner
from .shared import sys

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--boot-organizer":
            run_headless_organizer()
        elif sys.argv[1] == "--boot-cleaner":
            run_headless_cleaner()
    else:
        app = AutomationHub()
        app.mainloop()

if __name__ == "__main__":
    main()
