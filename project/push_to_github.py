import subprocess

project = '/Users/shireen/sales dashboard analysis /project'


def run(cmd):
    result = subprocess.run(
        cmd, cwd=project, capture_output=True, text=True, shell=True)
    print(f">>> {cmd}")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    print()
    return result


print("=" * 50)
print("SYNCING AND PUSHING TO GITHUB")
print("=" * 50)
print()

# pull remote changes first, allow unrelated histories
run('git pull origin master --allow-unrelated-histories --no-edit')

# push everything
run('git push origin master')

print("=" * 50)
print("DONE — Your repo:")
print("https://github.com/shireenmulayamwala-05/sales-dashboard-analysis")
print("=" * 50)
