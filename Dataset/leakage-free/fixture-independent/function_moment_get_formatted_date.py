import moment


def get_formatted_current_datetime(time_format: str = None) -> str:
    if time_format is None:
        raise ValueError("Error: time_format is required ('complete' or 'simple')")

    if time_format not in ['complete', 'simple']:
        raise ValueError("Error: time_format must be either 'complete' or 'simple'")

    now = moment
    if time_format == 'complete':
        return (
            f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {now}\n"
            f"Current User's Login: anonymous"
        )
    else:
        return str(now)

