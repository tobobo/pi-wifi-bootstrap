import os
import asyncio
from wifi_setup_server import start_wifi_setup_server
from stream_command import stream_command

async def run_command(cmd, env={}):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=dict(os.environ, **env))

    stdout, stderr = await proc.communicate()

    print(f'{cmd!r} exited with {proc.returncode}')

    if stdout:
        print(f'stdout:\n{stdout.decode()}')
    if stderr:
        print(f'stderr:\n{stderr.decode()}')

    return proc, stdout, stderr
    
async def set_credentials_and_reboot(ssid, psk):
  await run_command("bash scripts/setup_wifi_client.bash", { 'SSID': ssid, 'PSK': psk })
  await run_command("sudo systemctl reboot")


async def is_command_successful(cmd):
    proc, _, __ = await run_command(cmd)

    return proc.returncode == 0


async def is_ap():
    print("checking if ap")
    return await is_command_successful("systemctl status hostapd")

async def enable_ap_and_reboot():
    await run_command("bash scripts/setup_wifi_ap.bash")
    await run_command("sudo systemctl reboot")

async def has_wifi_connection():
    print("checking wifi connection")
    return await is_command_successful("bash scripts/check_wifi_connection.bash")


async def main():
    if await is_ap():
        print("access point, start wifi setup app")
        await start_wifi_setup_server(set_credentials_and_reboot)
    elif await has_wifi_connection():
        await stream_command(
            ["python3", "test_app.py"],
            lambda x: print("APP STDOUT: %s" % x),
            lambda x: print("APP STDERR: %s" % x),
        )
    else:
        print("no connection, enable ap and reboot")
        await enable_ap_and_reboot()


if __name__ == "__main__":
    asyncio.run(main())
