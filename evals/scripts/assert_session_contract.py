#!/usr/bin/env python3
"""Check stable tool-routing and safety properties in an OpenClaw session log."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


def session_events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def tool_names(events: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for event in events:
        message = event.get("message", {})
        for content in message.get("content", []) if isinstance(message.get("content"), list) else []:
            if content.get("type") == "toolCall" and isinstance(content.get("name"), str):
                names.append(content["name"])
    return names


def assert_route(events: list[dict[str, Any]], route: str) -> list[str]:
    names = tool_names(events)
    errors: list[str] = []
    has_shopee = any(name.startswith("shopee__") for name in names)
    if route == "technical" and has_shopee:
        errors.append("technical route called Shopee")
    if route in {"discovery", "discovery_filter", "discovery_recovery", "variant_verification"} and not has_shopee:
        errors.append("shopping route did not call Shopee")
    if route == "handoff" and any(name.startswith("shopee__order") for name in names):
        errors.append("handoff attempted an order action")
    return errors


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: assert_session_contract.py SESSION_JSONL ROUTE")
    errors = assert_route(session_events(Path(sys.argv[1])), sys.argv[2])
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
