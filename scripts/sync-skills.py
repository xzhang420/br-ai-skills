"""Cross-platform pull-only counterpart to sync-skills.ps1 (Python 3.8+)."""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess

EXPECTED_REMOTE = 'https://github.com/xzhang420/br-ai-skills.git'
MARKERS = ('index.lock', 'HEAD.lock', 'MERGE_HEAD', 'CHERRY_PICK_HEAD',
           'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'sequencer')


@contextmanager
def exclusive_lock(path):
    # Same local lock file as the PowerShell script; never remove an active lock.
    with path.open('a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == 'nt':
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def sync(repo, expected_remote=EXPECTED_REMOTE):
    repo = repo.resolve(strict=True)
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never')

    def git(*args):
        result = subprocess.run(['git', '-C', str(repo), *args], env=env,
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise RuntimeError(f'git {args[0]} failed: {result.stderr.strip()}')
        return result.stdout.strip()

    def ready():
        if git('branch', '--show-current') != 'main':
            raise RuntimeError('Checkout is not on main.')
        if git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}') != 'origin/main':
            raise RuntimeError('Upstream is not origin/main.')
        if git('status', '--porcelain=v1', '--untracked-files=all'):
            raise RuntimeError('Local tracked or untracked changes exist.')
        if any((git_dir / marker).exists() for marker in MARKERS):
            raise RuntimeError('Active Git operation or lock.')

    if Path(git('rev-parse', '--show-toplevel')).resolve() != repo:
        raise RuntimeError('Supplied path is not the repository root.')
    if git('remote', 'get-url', 'origin') != expected_remote:
        raise RuntimeError('Unexpected origin remote.')
    git_dir = Path(git('rev-parse', '--absolute-git-dir'))
    with exclusive_lock(git_dir / 'skills-auto-pull.lock'):
        ready()
        before = git('rev-parse', 'HEAD')
        git('fetch', '--quiet', 'origin', 'main')
        ready()
        if git('rev-parse', 'HEAD') != before:
            raise RuntimeError('HEAD changed during sync.')
        if int(git('rev-list', '--count', 'origin/main..HEAD')):
            raise RuntimeError('Local commits are ahead of or diverged from origin/main.')
        git('-c', 'merge.autostash=false', '-c', 'rebase.autostash=false',
            'pull', '--quiet', '--ff-only', '--no-rebase', '--no-autostash', 'origin', 'main')
        after = git('rev-parse', 'HEAD')
        ready()
    return {'status': 'up_to_date' if before == after else 'updated',
            'before': before, 'after': after, 'repository': str(repo)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--expected-remote', default=EXPECTED_REMOTE)
    args = parser.parse_args()
    try:
        print(json.dumps(sync(args.repo, args.expected_remote)))
    except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
        print(json.dumps({'status': 'needs_attention', 'message': str(error),
                          'repository': str(args.repo)}))
        raise SystemExit(1)
