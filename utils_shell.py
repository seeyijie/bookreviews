import subprocess


class Shell:
    """Run arbitrary shell commands with subprocess parameters"""

    def __init__(self, **kwargs) -> None:
        # eg Shell(shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.kwargs = kwargs

    def run(self, command: str) -> str:
        output = subprocess.run(command, **self.kwargs).stdout.decode()
        return output


def shell(command: str) -> str:
    """Convenience function to run arbitrary shell commands and return the output"""

    default_shell = Shell(shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return default_shell.run(command)
