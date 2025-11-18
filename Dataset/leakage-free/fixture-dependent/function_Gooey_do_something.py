import os
from gooey import Gooey, GooeyParser
from datetime import datetime, UTC


@Gooey(program_name="Gooey App", suppress_gooey=True)
def run_gooey_app(args=None, current_time=None):
    if not current_time or not isinstance(current_time, datetime):
        current_time = datetime.now(UTC)

    if os.environ.get("TESTING"):
        name = "User"
        if args and "--name" in args:
            idx = args.index("--name")
            if idx + 1 < len(args):
                name = args[idx + 1]
        return f"Gooey app ran successfully for {name} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        parser = GooeyParser(description="A simple Gooey app")
        parser.add_argument("--name", help="Enter your name", default="User")
        parsed_args = parser.parse_args(args=args)
        return f"Gooey app ran successfully for {parsed_args.name} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}"

