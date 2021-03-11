import subprocess

process = subprocess.Popen(['git', 'rev-parse', 'HEAD'], shell=False, stdout=subprocess.PIPE)
git_head_hash = str(process.communicate()[0].strip())[2:-1]

