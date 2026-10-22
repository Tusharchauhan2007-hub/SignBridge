"""
Custom Manual Command Manager for SignBridge.
Provides local persistent JSON storage, validation, execution, and testing
for personal gesture commands and macro actions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

COMMANDS_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "custom_commands.json"

DEFAULT_COMMANDS: List[Dict[str, Any]] = [
    {
        "id": "cmd_default_help",
        "name": "Emergency Assistance Call",
        "trigger": "HELP",
        "action_type": "Vocalize Speech",
        "payload": "Emergency: I require immediate assistance, please.",
        "enabled": True,
        "created_at": "2026-10-22 09:00:00",
        "description": "Speaks an urgent assistance request when HELP sign is recognized.",
    },
    {
        "id": "cmd_default_hello",
        "name": "Standard Everyday Greeting",
        "trigger": "HELLO",
        "action_type": "Vocalize Speech",
        "payload": "Hello everyone, hope you are having a wonderful day!",
        "enabled": True,
        "created_at": "2026-10-22 09:00:00",
        "description": "Vocalizes a warm greeting sentence when HELLO gesture is signed.",
    },
    {
        "id": "cmd_default_yes",
        "name": "Confirmation Affirmation",
        "trigger": "YES",
        "action_type": "Vocalize Speech",
        "payload": "Yes, I agree and confirm this choice.",
        "enabled": True,
        "created_at": "2026-10-22 09:00:00",
        "description": "Speaks a clear confirmation sentence when YES is signed.",
    },
    {
        "id": "cmd_default_thanks",
        "name": "Gratitude & Thanks",
        "trigger": "THANK_YOU",
        "action_type": "Translate to Hindi & Speak",
        "payload": "Thank you so much for your kind help and support.",
        "enabled": True,
        "created_at": "2026-10-22 09:00:00",
        "description": "Expresses gratitude and triggers bilingual translation.",
    },
]


class CustomCommandManager:
    """Manages persistent custom commands stored locally in data/custom_commands.json."""

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = Path(file_path) if file_path else COMMANDS_FILE_PATH
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Initialize the storage file with default starter commands if not present."""
        os.makedirs(self.file_path.parent, exist_ok=True)
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self._save_raw(DEFAULT_COMMANDS)

    def _save_raw(self, commands: List[Dict[str, Any]]) -> None:
        """Safely write command list to local disk."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=2, ensure_ascii=False)

    def load_commands(self) -> List[Dict[str, Any]]:
        """Load all saved commands from local JSON."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return DEFAULT_COMMANDS
        except Exception:
            return DEFAULT_COMMANDS

    def add_command(
        self,
        name: str,
        trigger: str,
        action_type: str,
        payload: str,
        description: str = "",
        enabled: bool = True,
    ) -> Tuple[bool, str]:
        """
        Validate and create a new custom command.
        Returns (success: bool, message: str).
        """
        name = name.strip()
        payload = payload.strip()
        trigger = trigger.strip().upper()

        if not name:
            return False, "Command name cannot be empty."
        if not payload:
            return False, "Action response or text cannot be empty."
        if not trigger:
            return False, "A trigger gesture or letter must be selected."

        commands = self.load_commands()

        # Check for duplicate names
        if any(c.get("name", "").lower() == name.lower() for c in commands):
            return False, f"A command with the name '{name}' already exists."

        cmd_id = f"cmd_{int(datetime.now().timestamp())}_{abs(hash(name)) % 1000}"
        new_cmd = {
            "id": cmd_id,
            "name": name,
            "trigger": trigger,
            "action_type": action_type,
            "payload": payload,
            "enabled": enabled,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description.strip() or f"Triggered when '{trigger}' is recognized.",
        }

        commands.append(new_cmd)
        self._save_raw(commands)
        return True, f"Command '{name}' created successfully."

    def update_command(
        self,
        cmd_id: str,
        name: str,
        trigger: str,
        action_type: str,
        payload: str,
        description: str = "",
        enabled: bool = True,
    ) -> Tuple[bool, str]:
        """Update an existing command by ID."""
        name = name.strip()
        payload = payload.strip()
        trigger = trigger.strip().upper()

        if not name:
            return False, "Command name cannot be empty."
        if not payload:
            return False, "Action response or text cannot be empty."

        commands = self.load_commands()
        found = False
        for c in commands:
            if c.get("id") == cmd_id:
                c["name"] = name
                c["trigger"] = trigger
                c["action_type"] = action_type
                c["payload"] = payload
                c["description"] = description.strip()
                c["enabled"] = enabled
                c["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break

        if not found:
            return False, f"Command with ID '{cmd_id}' not found."

        self._save_raw(commands)
        return True, f"Command '{name}' updated successfully."

    def toggle_command(self, cmd_id: str) -> Tuple[bool, str]:
        """Toggles a command between enabled and disabled."""
        commands = self.load_commands()
        new_state = False
        found = False
        for c in commands:
            if c.get("id") == cmd_id:
                c["enabled"] = not c.get("enabled", True)
                new_state = c["enabled"]
                found = True
                break

        if not found:
            return False, "Command not found."

        self._save_raw(commands)
        state_str = "enabled" if new_state else "disabled"
        return True, f"Command is now {state_str}."

    def delete_command(self, cmd_id: str) -> Tuple[bool, str]:
        """Deletes a command by ID."""
        commands = self.load_commands()
        initial_count = len(commands)
        commands = [c for c in commands if c.get("id") != cmd_id]

        if len(commands) == initial_count:
            return False, f"Command with ID '{cmd_id}' not found."

        self._save_raw(commands)
        return True, "Command deleted successfully."

    def get_command_by_trigger(self, trigger: str) -> Optional[Dict[str, Any]]:
        """Find the first active command mapped to a recognized sign trigger."""
        if not trigger:
            return None
        trigger_clean = trigger.strip().upper()
        for c in self.load_commands():
            if c.get("enabled", True) and c.get("trigger", "").upper() == trigger_clean:
                return c
        return None

