import asyncio
import subprocess
import time

class CommandExecutor:
    async def execute(self, command, timeout=300):
        start_time = time.time()
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                duration = time.time() - start_time
                
                return {
                    "command": command,
                    "output": stdout.decode() + stderr.decode(),
                    "exit_code": process.returncode,
                    "duration": round(duration, 2)
                }
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "command": command,
                    "output": "Error: Command timed out",
                    "exit_code": -1,
                    "duration": timeout
                }
        except Exception as e:
            return {
                "command": command,
                "output": f"Error: {str(e)}",
                "exit_code": -1,
                "duration": 0
            }
