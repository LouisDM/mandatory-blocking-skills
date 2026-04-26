"""
MB-Protocol Plugin for AutoGPT
================================
This plugin enforces Mandatory Blocking checkpoints in AutoGPT's command chain.

Usage:
    Add to AutoGPT's plugins directory and enable in .env:
    USE_MB_PROTOCOL=true
"""

from autogpt_plugin_template import AutoGPTPluginTemplate
from typing import Any, Dict, List, Optional, Tuple

class MBProtocolPlugin(AutoGPTPluginTemplate):
    """
    Enforces MB-Protocol checkpoints before and after critical commands.
    """

    def __init__(self):
        super().__init__()
        self._name = "MB-Protocol"
        self._version = "1.0.0"
        self._description = "Mandatory Blocking Protocol for reliable agent execution"
        self.blocking_commands = [
            "deploy", "git_commit", "write_file", "execute_python"
        ]

    def post_command(self, command_name: str, response: str) -> str:
        """
        BLOCKING checkpoint after critical commands.
        """
        if command_name in self.blocking_commands:
            # Enforce verification
            verification = self._verify_command(command_name, response)
            if not verification["passed"]:
                return (
                    f"[MB-Protocol BLOCKING] Command '{command_name}' failed verification.\n"
                    f"Error: {verification['error']}\n"
                    f"Required: Retry or execute fallback."
                )
        return response

    def _verify_command(self, command: str, response: str) -> Dict[str, Any]:
        """
        Verify command execution using empirical checks.
        """
        verifications = {
            "deploy": lambda r: "HTTP 200" in r or "deployed successfully" in r.lower(),
            "git_commit": lambda r: "committed" in r.lower() and r.count("+") > 0,
            "write_file": lambda r: "written" in r.lower(),
            "execute_python": lambda r: "error" not in r.lower() or "traceback" not in r.lower(),
        }

        checker = verifications.get(command, lambda r: True)
        passed = checker(response)

        return {
            "passed": passed,
            "error": None if passed else f"Verification failed for {command}",
            "command": command,
            "response_preview": response[:200] if response else ""
        }

    def can_handle_post_command(self) -> bool:
        return True
