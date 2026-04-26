#!/usr/bin/env python3
"""
MB-Protocol Verification Script
Automated experiment runner to collect reproducible data.

Usage:
    python run-experiment.py --mode baseline --count 5
    python run-experiment.py --mode mb-protocol --count 5
"""

import argparse
import json
import subprocess
import time
import sys
from datetime import datetime

API_BASE = "http://localhost:8000"


def run_curl(method, path, data=None):
    """Run curl and return parsed JSON."""
    cmd = ["curl", "-s", "-X", method, f"{API_BASE}{path}"]
    if data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return {"error": result.stderr}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout}


def reset_mock():
    """Reset the mock application."""
    run_curl("POST", "/reset")


def create_issue(title, description):
    """Create a test issue."""
    return run_curl("POST", "/api/issues", {"title": title, "description": description})


def check_comments(issue_id):
    """Check if issue has comments."""
    issue = run_curl("GET", f"/api/issues/{issue_id}")
    comments = issue.get("comments", [])
    return len(comments) > 0, comments


def run_single_experiment(mode, index):
    """Run one experiment iteration."""
    print(f"\n{'='*60}")
    print(f"Experiment {index + 1}/? — Mode: {mode}")
    print(f"{'='*60}")

    # Reset and create issue
    reset_mock()
    time.sleep(0.5)

    issue = create_issue(
        f"[{mode}] Test Todo Implementation #{index + 1}",
        "Implement a simple Todo CRUD API with FastAPI. Test it. Report results."
    )
    issue_id = issue.get("id")
    print(f"Created issue: {issue_id}")

    # Prompt the user to run their Agent
    prompt_file = f"prompts/{mode}-prompt.md"
    print(f"\n>>> NEXT: Copy the prompt from {prompt_file}")
    print(f">>> Replace {{ISSUE_ID}} with: {issue_id}")
    print(">>> Run it through your Agent (Claude Code, Cursor, etc.)")
    print(">>> After Agent finishes, press Enter to check results...")
    input()

    # Check results
    has_comments, comments = check_comments(issue_id)
    issue_status = run_curl("GET", f"/api/issues/{issue_id}").get("status", "unknown")

    result = {
        "mode": mode,
        "index": index + 1,
        "issue_id": issue_id,
        "has_comments": has_comments,
        "comment_count": len(comments),
        "issue_status": issue_status,
        "timestamp": datetime.now().isoformat()
    }

    print(f"\nResults:")
    print(f"  Has Comments: {has_comments}")
    print(f"  Comment Count: {len(comments)}")
    print(f"  Issue Status: {issue_status}")
    print(f"  Comments: {[c.get('content', '')[:100] for c in comments]}")

    return result


def main():
    parser = argparse.ArgumentParser(description="MB-Protocol Verification Experiment")
    parser.add_argument("--mode", choices=["baseline", "mb-protocol"], required=True,
                        help="Experiment mode: baseline (no MB-Protocol) or mb-protocol (with MB-Protocol)")
    parser.add_argument("--count", type=int, default=5,
                        help="Number of experiments to run (default: 5)")
    parser.add_argument("--output", default="results.json",
                        help="Output file for results (default: results.json)")
    args = parser.parse_args()

    print("="*60)
    print("MB-Protocol Verification Experiment")
    print("="*60)
    print(f"Mode: {args.mode}")
    print(f"Count: {args.count}")
    print(f"API: {API_BASE}")
    print()
    print("PREREQUISITES:")
    print("  1. Start the mock app: cd mock-app && uvicorn main:app --port 8000")
    print("  2. Ensure your AI Agent can access localhost:8000")
    print()
    confirm = input("Ready? (yes/no): ")
    if confirm.lower() != "yes":
        print("Aborted.")
        sys.exit(0)

    results = []
    for i in range(args.count):
        result = run_single_experiment(args.mode, i)
        results.append(result)

    # Save results
    with open(args.output, "w") as f:
        json.dump({
            "mode": args.mode,
            "count": args.count,
            "results": results,
            "summary": {
                "total": len(results),
                "with_comments": sum(1 for r in results if r["has_comments"]),
                "without_comments": sum(1 for r in results if not r["has_comments"]),
                "comment_rate": sum(1 for r in results if r["has_comments"]) / len(results) * 100 if results else 0
            }
        }, f, indent=2)

    print(f"\n{'='*60}")
    print("EXPERIMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {args.output}")
    print(f"\nSummary:")
    print(f"  Total: {len(results)}")
    print(f"  With Comments: {sum(1 for r in results if r['has_comments'])}")
    print(f"  Without Comments: {sum(1 for r in results if not r['has_comments'])}")
    print(f"  Comment Rate: {sum(1 for r in results if r['has_comments']) / len(results) * 100:.1f}%")


if __name__ == "__main__":
    main()
