#!/usr/bin/env python3
"""Install shared Workflow 1 on this device. Dry-run by default; no Git actions."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

MARKER = '.workflow1-install.json'
IGNORES = shutil.ignore_patterns('__pycache__', '*.pyc', '.venv', '.env*', '.git', '.workflow1', 'runs', MARKER)


def source_files(root):
    files = {}
    for directory, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.venv', '.git', '.workflow1', 'runs')]
        for name in names:
            if name == MARKER or name.startswith('.env') or name.endswith('.pyc'):
                continue
            path = Path(directory) / name
            files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def managed_copy(path, source):
    try:
        data = json.loads((path / MARKER).read_text(encoding='utf-8'))
        return data.get('source') == str(source)
    except (OSError, ValueError):
        return False


def install_skill(dest, source, strategy):
    if strategy != 'copy':
        try:
            dest.symlink_to(source, target_is_directory=True)
            return 'symlink'
        except OSError as exc:
            if strategy == 'link':
                raise RuntimeError('Symlink unavailable; retry --skill-install copy.') from exc
            if dest.exists() or dest.is_symlink():
                raise RuntimeError('Skill destination appeared while linking; inspect it before retrying.') from exc
            print('Symlink unavailable; installing a managed copy instead.')
    shutil.copytree(source, dest, ignore=IGNORES)
    (dest / MARKER).write_text(json.dumps({'source': str(source), 'files': source_files(source)}, indent=2) + '\n', encoding='utf-8')
    return 'copy'


def install(source, home, codex, *, apply=False, replace_legacy=False, strategy='auto'):
    source, home, codex = source.resolve(), home.resolve(), codex.resolve()
    backup = codex / 'backups' / ('workflow1-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    actions = []
    shared_entry = codex / 'skills' / source.name
    reuse = shared_entry.exists() and shared_entry.resolve() == source
    entry = home / '.agents/skills/workflow-1'
    candidates = [entry, home / '.agents/skills/godzilla-workflow-1',
                  codex / 'skills/godzilla-workflow-1', codex / 'skills/workflow-1']
    seen = set()
    for old in candidates:
        if old == shared_entry or old in seen or not (old.exists() or old.is_symlink()):
            continue
        seen.add(old)
        same_source = old.resolve() == source
        if old == entry and same_source and not reuse:
            continue
        if old == entry and not reuse and not old.is_symlink() and managed_copy(old, source):
            if source_files(old) == source_files(source):
                continue
        elif not same_source and not replace_legacy:
            raise RuntimeError('Existing Workflow 1 entry differs: ' + str(old) + '; preview --replace-legacy to back it up.')
        actions.append(('retire', old, None))
    retired = {dest for kind, dest, _ in actions if kind == 'retire'}
    if not reuse and (entry in retired or not (entry.exists() or entry.is_symlink())):
        actions.append(('skill', entry, source))
    for src in sorted((source / 'config').glob('*.toml')):
        dest = codex / src.name
        if not dest.exists() or dest.read_bytes() != src.read_bytes():
            actions.append(('copy', dest, src))
    for src in sorted((source / 'config/agents').glob('*.toml')):
        dest = codex / 'agents' / src.name
        if not dest.exists() or dest.read_bytes() != src.read_bytes():
            actions.append(('copy', dest, src))
    settings = codex / 'workflow1-local.json'
    if not settings.exists():
        actions.append(('text', settings, json.dumps({'schema_version': 1, 'commands': {}, 'env_file': None}, indent=2) + '\n'))
    guidance = codex / 'AGENTS.md'
    marker = '## Workflow 1 entry point'
    previous = guidance.read_text(encoding='utf-8') if guidance.exists() else ''
    reference = (shared_entry if reuse else entry).as_posix()
    addition = (marker + '\nWhen the user invokes Workflow 1, read `' + reference +
                '/SKILL.md`. It defines the workflow, effort modes, state records and provider boundaries.\n')
    if marker in previous:
        updated = re.sub(r'(?ms)^## Workflow 1 entry point\n.*?(?=^## |\Z)',
                         lambda _: addition + '\n', previous).rstrip() + '\n'
    else:
        updated = previous.rstrip() + '\n\n' + addition
    if updated != previous:
        actions.append(('text', guidance, updated))
    for kind, dest, _ in actions:
        if kind not in ('retire', 'skill') and dest.is_symlink():
            raise RuntimeError('Refusing to overwrite a config symlink: ' + str(dest))
    for kind, dest, _ in actions:
        print(kind.upper(), dest)
    print('Discovery:', shared_entry if reuse else entry)
    if not apply:
        print('DRY RUN; no changes.')
        return {'actions': len(actions), 'discovery': str(shared_entry if reuse else entry)}
    base = codex / 'config.toml'
    before = hashlib.sha256(base.read_bytes()).hexdigest() if base.exists() else None
    manifest = []
    for kind, dest, src in actions:
        saved = None
        if dest.exists() or dest.is_symlink():
            try:
                relative = dest.relative_to(home)
            except ValueError:
                relative = Path('external-codex-home') / dest.relative_to(codex)
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            if kind == 'retire':
                shutil.move(str(dest), str(saved))
            else:
                shutil.copy2(dest, saved)
        mode = None
        if kind != 'retire':
            dest.parent.mkdir(parents=True, exist_ok=True)
            if kind == 'skill':
                mode = install_skill(dest, source, strategy)
            elif kind == 'copy':
                shutil.copy2(src, dest)
            elif kind == 'text':
                dest.write_text(src, encoding='utf-8')
        manifest.append({'action': kind, 'path': str(dest), 'backup': str(saved) if saved else None, 'install_mode': mode})
        backup.mkdir(parents=True, exist_ok=True)
        (backup / 'manifest.json').write_text(json.dumps({'actions': manifest, 'base_config_sha256': before}, indent=2) + '\n', encoding='utf-8')
    after = hashlib.sha256(base.read_bytes()).hexdigest() if base.exists() else None
    if before != after:
        raise RuntimeError('Unexpected base configuration change')
    if actions:
        print('Backup manifest:', backup / 'manifest.json')
    print('Installed. Base config unchanged. No Git actions performed.')
    return {'actions': len(actions), 'discovery': str(shared_entry if reuse else entry)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace-legacy', action='store_true', help='Back up previous standalone/device-owned Workflow 1 entries')
    p.add_argument('--skill-install', choices=('auto', 'link', 'copy'), default='auto', help='auto tries symlink then copy; copy needs rerunning after updates')
    p.add_argument('--home', type=Path, default=Path.home(), help='Alternate home for installer tests')
    args = p.parse_args()
    source = Path(__file__).resolve().parent.parent
    home = args.home.expanduser().resolve()
    codex = Path(os.environ.get('CODEX_HOME', str(home / '.codex'))).expanduser()
    if args.home != Path.home():
        codex = home / '.codex'
    try:
        install(source, home, codex, apply=args.apply, replace_legacy=args.replace_legacy, strategy=args.skill_install)
    except (RuntimeError, OSError) as exc:
        raise SystemExit(str(exc)) from None


if __name__ == '__main__':
    main()
