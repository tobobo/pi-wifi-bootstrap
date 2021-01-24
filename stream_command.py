import asyncio

async def _read_stream(stream, cb):
    print("read stream")
    while True:
        print("awaiting line")
        line = await stream.readline()
        if line:
            print("cb line")
            cb(line)
        else:
            print("no line")
            break

async def _stream_subprocess(cmd, stdout_cb, stderr_cb):  
    process = await asyncio.create_subprocess_exec(*cmd,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb)
    ])
    return await process.wait()


async def stream_command(cmd, stdout_cb, stderr_cb):  
    await _stream_subprocess(
            cmd,
            stdout_cb,
            stderr_cb,
    )
