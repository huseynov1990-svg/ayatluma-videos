# Zagruzka gotovykh fajlov v GitHub (vetka dnya d-YYYY-MM-DD) + udalenie vetok starshe 5 dney.
# python upload.py <repo_dir> <papka_v_repo> <fayl1> [fayl2 ...]   -> pechataet publichnye ssylki
import sys, os, subprocess, shutil, datetime, re
repo, sub, files = sys.argv[1], sys.argv[2], sys.argv[3:]
OWNER_REPO = 'huseynov1990-svg/ayatluma-videos'
today = datetime.date.today(); br = 'd-%s' % today.isoformat()
def g(*a, check=True): return subprocess.run(['git', '-C', repo] + list(a), check=check, capture_output=True, text=True)
work = os.path.join('/tmp', 'upl_' + br)
if not os.path.exists(work):
    r = subprocess.run(['git', 'clone', '--depth', '1', '--branch', br, 'https://github.com/%s' % OWNER_REPO, work], capture_output=True, text=True)
    if r.returncode != 0:
        os.makedirs(work, exist_ok=True)
        subprocess.run(['git', 'init', '-q', '-b', br, work], check=True)
        subprocess.run(['git', '-C', work, 'remote', 'add', 'origin', 'https://github.com/%s' % OWNER_REPO], check=True)
dst = os.path.join(work, sub); os.makedirs(dst, exist_ok=True)
for f in files: shutil.copy(f, os.path.join(dst, os.path.basename(f)))
subprocess.run(['git', '-C', work, 'add', '-A'], check=True)
subprocess.run(['git', '-C', work, '-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com', 'commit', '-qm',
                'Videos %s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>' % today], check=False)
r = subprocess.run(['git', '-C', work, '-c', 'push.negotiate=true', 'push', '-u', 'origin', br], capture_output=True, text=True)
print(r.stdout[-300:], r.stderr[-300:])
for f in files:
    print('URL https://raw.githubusercontent.com/%s/%s/%s/%s' % (OWNER_REPO, br, sub, os.path.basename(f)))
# udalit vetki dney starshe 5 dney (i staruyu vetku media)
ls = subprocess.run(['git', 'ls-remote', '--heads', 'https://github.com/%s' % OWNER_REPO], capture_output=True, text=True).stdout
for line in ls.splitlines():
    m = re.search(r'refs/heads/(d-(\d{4}-\d{2}-\d{2})|media)$', line)
    if not m: continue
    name = m.group(1)
    old = name == 'media' and today >= datetime.date(2026, 11, 20)
    if m.group(2): old = (today - datetime.date.fromisoformat(m.group(2))).days > 5
    if old:
        rr = subprocess.run(['git', '-C', work, 'push', 'origin', '--delete', name], capture_output=True, text=True)
        print('UDALENA vetka', name, 'ok' if rr.returncode == 0 else rr.stderr[-200:])
