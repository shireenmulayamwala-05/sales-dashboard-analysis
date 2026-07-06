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
print("PUSHING PROJECT TO GITHUB")
print("=" * 50)
print()

# configure git identity (needed on some machines)
run('git config user.email "shireenmulayamwala@gmail.com"')
run('git config user.name "shireenmulayamwala-05"')

# stage all new and changed files
run('git add .')

# show what will be committed
run('git status')

# commit
run('git commit -m "Add complete analytics project: EDA, SQL, Streamlit dashboard, reports, docs"')

# push
run('git push origin master')

print("=" * 50)
print("DONE — Check your GitHub repo:")
print("https://github.com/shireenmulayamwala-05/sales-dashboard-analysis")
print("=" * 50)
