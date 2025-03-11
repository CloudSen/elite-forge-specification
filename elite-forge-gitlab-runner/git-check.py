import sys
import re
import subprocess
import os

# 提交信息格式正则
COMMIT_MSG_PATTERN = r'^(feat|fix|test|refactor)\(#\d+\): .+|^(doc|build|style)(\(#\d+\))?: .+'
MERGE_COMMIT_PATTERN = r'^Merge (branch|commit) .+'

def print_error_message(commit_msg):
    """打印错误信息，包含提交信息格式要求和示例"""
    print(f"[ERROR] 提交信息格式错误！请使用以下格式(注意空格，必须用英文符号)：")
    print(f"   [type](#需求id): 提交信息")
    print(f"""允许的 type:
        feat, fix, test, doc, build, refactor, style""")
    print(f"""必须带ID的 type:
        feat, fix, test, refactor""")
    print(f"""合规的案例：
        feat(#123): 添加xxx功能
        fix(#321): 修复xxxbug
        style: 调整代码格式
        doc: 更新xxx文档
        doc(#789): 更新xxx注释
        build: 更新xxx依赖
        build(#789): 更新xxx脚本
        refactor(#456): 重构xxx代码""")
    print(f"\n[ERROR] 你的提交信息:\n   {commit_msg}\n") 
    sys.exit(1)

def fetch_target_branch():
    """确保目标分支在本地可用"""
    target_branch = os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", "main")
    try:
        subprocess.run(["git", "fetch", "--no-tags", "--update-head-ok", "origin", target_branch], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 无法获取远程分支 {target_branch}: {e.stderr}")
        sys.exit(1)

def get_mr_commits():
    """获取当前 MR 里的所有提交信息"""
    target_branch = os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", "master")
    source_branch = os.getenv("CI_COMMIT_REF_NAME", "HEAD")

    subprocess.run(["git", "fetch", "--no-tags", "--force", "origin", target_branch], check=True)
    subprocess.run(["git", "fetch", "--no-tags", "--force", "origin", source_branch], check=True)
    subprocess.run(["git", "reset", "--hard", f"origin/{source_branch}"], check=True)  # 强制同步

    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%s", f"origin/{target_branch}..origin/{source_branch}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split("\n")
        return [commit for commit in commits if commit]
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 无法获取 MR 提交记录: {e.stderr}")
        sys.exit(1)

def validate_commit_messages():
    """检查 MR 里的所有提交信息是否符合规范"""
    fetch_target_branch()
    commits = get_mr_commits()

    source_branch = os.getenv("CI_COMMIT_REF_NAME", "HEAD")

    # 跳过 release/* 分支的 squash 校验
    if source_branch.startswith("release/"):
        print(f"[INFO] 跳过 {source_branch} 分支的 squash 校验。")
        sys.exit(0)

    if len(commits) > 1:
        print(f"[ERROR] 你有 {len(commits)} 个提交，必须合并为一个（squash）。")
        sys.exit(1)

    commit_msg = commits[0]

    if re.match(MERGE_COMMIT_PATTERN, commit_msg):
        print("[INFO] 跳过合并提交的校验。")
        sys.exit(0)

    if not re.match(COMMIT_MSG_PATTERN, commit_msg):
        print_error_message(commit_msg)

    print("[OK] 提交信息符合规范！")

if __name__ == "__main__":
    validate_commit_messages()