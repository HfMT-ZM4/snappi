import logging
import asyncio
from subprocess import CalledProcessError


async def check_call(cmd, **kwargs):
    logging.debug(f'check_call({cmd}, {kwargs})')
    process = await asyncio.create_subprocess_shell(cmd, **kwargs)
    return_code = await process.wait()
    if return_code != 0:
        raise CalledProcessError(return_code, cmd)

