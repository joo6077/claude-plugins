"""Credential lifecycle for measurements, never a production implementation.

Only copy authentication into a private writable directory under the measurement
run. Never print credential bytes or include them in evidence. Preserve sessions.
"""
from contextlib import contextmanager
import os
from pathlib import Path
import signal
import stat
import tempfile


def mode(path):
    return stat.S_IMODE(Path(path).stat().st_mode)


def secret_paths(root, secrets, exclude=()):
    excluded={Path(p).absolute() for p in exclude}
    found=[]
    for path in Path(root).rglob('*'):
        if path.absolute() in excluded or not path.is_file():
            continue
        try:
            data=path.read_bytes()
        except OSError:
            raise RuntimeError('credential scan unreadable file: '+str(path)) from None
        if any(value and value in data for value in secrets):
            found.append(str(path))
    return sorted(found)


@contextmanager
def writable_home(source, run):
    """0600 from creation, including when interrupted during copying/login/exec."""
    source=Path(source)
    home=Path(tempfile.mkdtemp(prefix='live-home-',dir=run))
    home.chmod(0o700)
    auth=home/'auth.json'
    handlers={}
    def interrupted(signum, frame):
        raise InterruptedError('measurement interrupted signal='+str(signum))
    try:
        for sig in (signal.SIGINT,signal.SIGTERM):
            handlers[sig]=signal.signal(sig,interrupted)
        with (source/'auth.json').open('rb') as src:
            fd=os.open(auth,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as dst:
                dst.write(src.read())
        (home/'config.toml').write_bytes((source/'config.toml').read_bytes())
        if mode(auth)!=0o600:
            raise RuntimeError('copied auth mode is not 600')
        yield home
    finally:
        # No recursive shell deletion; credentials alone are removed, logs survive.
        for sig in handlers:
            signal.signal(sig,signal.SIG_IGN)
        try:
            auth.unlink(missing_ok=True)
        finally:
            for sig,handler in handlers.items():
                signal.signal(sig,handler)
