import click


def log_status(count, label):
    """
    Log the output of a click command

    :param count: int
    :param label: str
    :return: None
    """
    click.echo(f"Created: {count} {label}")

    return None
