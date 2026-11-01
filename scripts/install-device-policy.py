"""Install a bounded global instruction block and local device identity.

Does not change permissions, Git state, skills links, or schedules.
"""
import argparse
import json
import os
import re
from pathlib import Path

BEGIN = '<!-- br-ai-skills:begin -->'
END = '<!-- br-ai-skills:end -->'


def merge_block(existing, block):
    if existing.count(BEGIN) != existing.count(END) or existing.count(BEGIN) > 1:
        raise ValueError('Ambiguous managed markers; inspect AGENTS.md manually.')
    if BEGIN in existing:
        start = existing.index(BEGIN)
        finish = existing.index(END) + len(END)
        if finish <= start:
            raise ValueError('Reversed managed markers.')
        return existing[:start] + block.strip() + existing[finish:]
    return existing + ('\n\n' if existing else '') + block.strip() + '\n'


def install(repo, codex_dir, device):
    repo = repo.resolve()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', device):
        raise ValueError('Device must be a lowercase ownership prefix.')
    if not (repo / 'AGENTS.md').is_file() or not (repo / 'third-party-skills.toml').is_file():
        raise ValueError('Not the shared skills checkout.')
    override = codex_dir / 'AGENTS.override.md'
    if override.is_file() and override.read_text(encoding='utf-8-sig').strip():
        raise ValueError('AGENTS.override.md would hide AGENTS.md; reconcile manually.')
    agents = codex_dir / 'AGENTS.md'
    identity = codex_dir / 'skills-device.json'
    expected = {'device': device, 'repository': repo.as_posix()}
    if identity.exists() and json.loads(identity.read_text(encoding='utf-8')) != expected:
        raise ValueError('Device identity already differs; reconcile manually.')
    block = (repo / 'scripts/templates/global-skills-instructions.md').read_text(encoding='utf-8')
    block = block.replace('{{DEVICE}}', device).replace('{{REPO}}', repo.as_posix())
    old = agents.read_text(encoding='utf-8-sig') if agents.exists() else ''
    new = merge_block(old, block)
    codex_dir.mkdir(parents=True, exist_ok=True)
    if old != new:
        # Preserve the original once; never overwrite a previous backup.
        backup = codex_dir / 'AGENTS.before-skills-policy.md.bak'
        if agents.exists() and not backup.exists():
            with backup.open('xb') as handle:
                handle.write(agents.read_bytes())
        agents.write_text(new, encoding='utf-8')
    if not identity.exists():
        identity.write_text(json.dumps(expected, indent=2) + '\n', encoding='utf-8')
    return {'status': 'installed' if old != new else 'up_to_date',
            'instructions': str(agents), 'device': device, 'repository': str(repo),
            'schedules_installed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', required=True)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--codex-dir', type=Path,
                        default=Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')))
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.repo, args.codex_dir, args.device)))
    except (OSError, ValueError) as error:
        print(json.dumps({'status': 'needs_attention', 'message': str(error)}))
        raise SystemExit(1)
