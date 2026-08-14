import gifos
from datetime import datetime
import os
import requests

# ============================================
# Terminal GIF with GitHub Stats
# ============================================
# 
# REQUIREMENTS:
# 1. Create a .env file in the project folder
# 2. Add: GITHUB_TOKEN=your_token_here
#
# To create the token:
# - Go to: https://github.com/settings/tokens
# - Click "Generate new token (classic)"
# - Select only: read:user
# - Copy the token and add it to .env
# ============================================

# Auto-detected from GitHub Actions context; falls back to env var or default.
USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "dbuzatto"
)

# Function to fetch real number of repos
def get_total_repos(username):
    try:
        headers = {}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json().get("public_repos", 0)
    except Exception:
        pass
    return None

# Try to fetch GitHub statistics
try:
    github_stats = gifos.utils.fetch_github_stats(user_name=USERNAME)
    has_stats = github_stats is not None
    if not has_stats:
        print("Warning: Could not fetch GitHub stats")
        print("Configure GITHUB_TOKEN in .env file")
except Exception as e:
    print(f"Warning: Error fetching GitHub stats: {e}")
    print("Using example data...")
    has_stats = False
    github_stats = None

# Fetch real number of repos
total_repos = get_total_repos(USERNAME)

# Terminal settings
t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)

# -- Initial prompt --
t.set_prompt(f"\x1b[91m{USERNAME}\x1b[0m@\x1b[93mgithub\x1b[0m ~> ")

# -- Boot sequence --
t.gen_text("Initializing terminal...", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m System ready", row_num=2)
t.clone_frame(10)

# -- Command to view stats --
t.gen_prompt(row_num=3)
t.gen_typing_text("github-stats --user " + USERNAME, row_num=3, contin=True, speed=1)
t.clone_frame(5)

# -- Display statistics --
t.gen_text("", row_num=4)
t.gen_text(f"\x1b[96m=== GitHub Stats for {USERNAME} ===\x1b[0m", row_num=5)
t.clone_frame(3)

if has_stats:
    repos_count = total_repos if total_repos else github_stats.total_repo_contributions
    stats_lines = [
        f"\x1b[93mName:\x1b[0m        {github_stats.account_name or USERNAME}",
        f"\x1b[93mFollowers:\x1b[0m   {github_stats.total_followers}",
        f"\x1b[93mStars:\x1b[0m       {github_stats.total_stargazers}",
        f"\x1b[93mCommits:\x1b[0m     {github_stats.total_commits_last_year} (last year)",
        f"\x1b[93mPRs:\x1b[0m         {github_stats.total_pull_requests_made}",
        f"\x1b[93mIssues:\x1b[0m      {github_stats.total_issues}",
        f"\x1b[93mRepos:\x1b[0m       {repos_count}",
        f"\x1b[93mRank:\x1b[0m        {github_stats.user_rank.level} ({github_stats.user_rank.percentile:.1f}%)",
    ]
    
    # Top languages
    if github_stats.languages_sorted:
        top_langs = github_stats.languages_sorted[:3]
        langs_str = ", ".join([f"{lang[0]} ({lang[1]}%)" for lang in top_langs])
        stats_lines.append(f"\x1b[93mTop Langs:\x1b[0m   {langs_str}")
else:
    # Example data
    stats_lines = [
        f"\x1b[93mName:\x1b[0m        {USERNAME}",
        "\x1b[93mFollowers:\x1b[0m   --",
        "\x1b[93mStars:\x1b[0m       --",
        "\x1b[93mCommits:\x1b[0m     -- (configure GITHUB_TOKEN)",
        "\x1b[93mPRs:\x1b[0m         --",
        "\x1b[93mIssues:\x1b[0m      --",
        "\x1b[93mRepos:\x1b[0m       --",
        "\x1b[93mRank:\x1b[0m        --",
    ]

for i, line in enumerate(stats_lines):
    t.gen_text(line, row_num=6+i)
    t.clone_frame(3)

t.clone_frame(10)
t.gen_text("\x1b[96m================================\x1b[0m", row_num=6+len(stats_lines))
t.clone_frame(15)

# -- Clear and Skills --
t.gen_prompt(row_num=7+len(stats_lines))
t.gen_typing_text("clear", row_num=7+len(stats_lines), contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m=== Tech Stack ===\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94miOS:\x1b[0m         ", "Swift, UIKit, SwiftUI"),
    ("\x1b[94mApple:\x1b[0m       ", "MapKit, CallKit, Core Location"),
    ("\x1b[94mApps:\x1b[0m        ", "App Store, maps, chat, calling"),
    ("\x1b[94mNow:\x1b[0m         ", "Easypaisa iOS"),
    ("\x1b[94mBackend:\x1b[0m     ", "Node.js, TypeScript"),
    ("\x1b[94mTools:\x1b[0m       ", "Xcode, Git, GitHub Actions"),
    ("\x1b[94mOS:\x1b[0m          ", "iOS, macOS"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text("\x1b[96m==================\x1b[0m", row_num=4+len(skills))
t.clone_frame(5)

# -- Final message --
final_row = 5 + len(skills)
t.gen_prompt(row_num=final_row)
t.gen_typing_text("echo 'hashimkhan.dev'", row_num=final_row, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[92mhashimkhan.dev\x1b[0m", row_num=final_row+1)
t.clone_frame(40)

# Generate the GIF
t.gen_gif()

print("\n GIF generated: output.gif")
print("\nTo use in your README.md:")
print('![Terminal GIF](./output.gif)')
