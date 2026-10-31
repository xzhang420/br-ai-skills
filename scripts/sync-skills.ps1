param(
    [string]$RepoPath = (Split-Path -Parent $PSScriptRoot),
    [string]$ExpectedRemote = 'https://github.com/xzhang420/br-ai-skills.git'
)

# Pull only. Never stash, rebase, commit, push, reset, or discard local work.
$ErrorActionPreference = 'Stop'
$env:GIT_TERMINAL_PROMPT = '0'
$env:GCM_INTERACTIVE = 'Never'
$syncLock = $null
$exitCode = 0

function Invoke-SyncGit {
    param([string[]]$GitArgs)
    $output = @(& git -C $RepoPath @GitArgs 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($GitArgs -join ' '): $($output -join ' ')"
    }
    return ($output -join "`n").Trim()
}

function Assert-SyncReady {
    if ((Invoke-SyncGit @('branch', '--show-current')) -ne 'main') {
        throw 'Skipped: checkout is not on main.'
    }
    if ((Invoke-SyncGit @('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')) -ne 'origin/main') {
        throw 'Skipped: upstream is not origin/main.'
    }
    if (Invoke-SyncGit @('status', '--porcelain=v1', '--untracked-files=all')) {
        throw 'Skipped: local tracked or untracked changes exist.'
    }
    foreach ($marker in @('index.lock', 'HEAD.lock', 'MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'sequencer')) {
        if (Test-Path -LiteralPath (Join-Path $script:gitDirectory $marker)) {
            throw "Skipped: Git operation or lock exists ($marker)."
        }
    }
}

try {
    $RepoPath = (Resolve-Path -LiteralPath $RepoPath).Path
    $root = Invoke-SyncGit @('rev-parse', '--show-toplevel')
    if ([IO.Path]::GetFullPath($root) -ne [IO.Path]::GetFullPath($RepoPath)) {
        throw 'Skipped: supplied directory is not the repository root.'
    }
    $remote = Invoke-SyncGit @('remote', 'get-url', 'origin')
    if ($remote -ne $ExpectedRemote) { throw 'Skipped: unexpected origin remote.' }
    $script:gitDirectory = Invoke-SyncGit @('rev-parse', '--absolute-git-dir')
    # File remains locally; the open handle, not file existence, is the lock.
    $syncLock = [IO.File]::Open((Join-Path $script:gitDirectory 'skills-auto-pull.lock'),
        [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    Assert-SyncReady
    $before = Invoke-SyncGit @('rev-parse', 'HEAD')
    Invoke-SyncGit @('fetch', '--quiet', 'origin', 'main') | Out-Null
    Assert-SyncReady
    if ((Invoke-SyncGit @('rev-parse', 'HEAD')) -ne $before) {
        throw 'Skipped: HEAD changed during the sync check.'
    }
    $ahead = [int](Invoke-SyncGit @('rev-list', '--count', 'origin/main..HEAD'))
    if ($ahead -gt 0) { throw 'Skipped: local commits are ahead of or diverged from origin/main.' }
    Invoke-SyncGit @('-c', 'merge.autostash=false', '-c', 'rebase.autostash=false',
        'pull', '--quiet', '--ff-only', '--no-rebase', '--no-autostash', 'origin', 'main') | Out-Null
    $after = Invoke-SyncGit @('rev-parse', 'HEAD')
    Assert-SyncReady
    [ordered]@{ status = $(if ($before -eq $after) { 'up_to_date' } else { 'updated' });
        before = $before; after = $after; repository = $RepoPath } | ConvertTo-Json -Compress
} catch {
    $exitCode = 1
    [ordered]@{ status = 'needs_attention'; message = $_.Exception.Message;
        repository = $RepoPath } | ConvertTo-Json -Compress
} finally {
    if ($null -ne $syncLock) { $syncLock.Dispose() }
}
exit $exitCode
