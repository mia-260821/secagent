

from pydantic import BaseModel
import typing
import subprocess


class CmdResult(BaseModel):
    stdout: typing.Union[typing.List[str], None, str]
    stderr: typing.Union[typing.List[str], None, str]
    returnCode: int



def execute_shell(command_name: str, *command_args: str) -> CmdResult:

    # Avoid shell=True for security when possible
    cmd = [command_name, *command_args]

    # Start the process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Wait for completion and collect output
    stdout, stderr = process.communicate()

    return CmdResult(stdout=stdout, stderr=stderr, returnCode=process.returncode)