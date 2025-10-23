import argparse
from huggingface_hub import HfApi, create_repo
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_id', required=True, help='e.g., PhenoX-Chappy/Archive-2025')
    parser.add_argument('--src_files', required=True, help='Comma-separated files to upload')
    parser.add_argument('--repo_type', default='space')
    parser.add_argument('--exist_ok', action='store_true')
    args = parser.parse_args()

    api = HfApi()
    # Ensure repo exists (Space, sdk=static)
    try:
        create_repo(args.repo_id, repo_type=args.repo_type, exist_ok=True, space_sdk='static')
    except Exception:
        pass

    for f in args.src_files.split(','):
        f = f.strip()
        p = Path(f)
        if not p.exists():
            print(f"[warn] missing file: {f}")
            continue
        path_in_repo = p.name  # upload to root
        api.upload_file(
            path_or_fileobj=str(p),
            path_in_repo=path_in_repo,
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            commit_message=f"Sync {p.name}"
        )
        print(f"[ok] uploaded: {p.name}")

if __name__ == '__main__':
    main()