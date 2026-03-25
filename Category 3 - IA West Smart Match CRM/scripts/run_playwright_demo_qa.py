from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://127.0.0.1:8501"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "playwright"
SUMMARY_PATH = OUTPUT_DIR / "2026-03-25-summary.json"


def get_route(url: str) -> str | None:
    return parse_qs(urlparse(url).query).get("route", [None])[0]


def body_text(page: Page) -> str:
    return page.locator("body").inner_text(timeout=20_000)


def wait_for_body_contains(page: Page, substrings: list[str], timeout_ms: int = 90_000) -> str:
    deadline = time.time() + timeout_ms / 1000
    last_text = ""
    while time.time() < deadline:
        try:
            last_text = body_text(page)
        except Exception:
            page.wait_for_timeout(1000)
            continue
        if all(part in last_text for part in substrings):
            return last_text
        page.wait_for_timeout(1000)
    raise AssertionError(
        "Missing text {}. Last body sample: {!r}".format(substrings, last_text[:1200])
    )


def wait_for_route(page: Page, expected: str, timeout_ms: int = 90_000) -> str:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        route = get_route(page.url)
        if route == expected:
            return page.url
        page.wait_for_timeout(500)
    raise AssertionError(f"Expected route={expected!r}, got url={page.url!r}")


def wait_for_regex(page: Page, pattern: str, timeout_ms: int = 45_000) -> str:
    regex = re.compile(pattern)
    deadline = time.time() + timeout_ms / 1000
    last_text = ""
    while time.time() < deadline:
        last_text = body_text(page)
        match = regex.search(last_text)
        if match:
            return match.group(0)
        page.wait_for_timeout(1000)
    raise AssertionError(
        "Pattern {!r} not found. Last body sample: {!r}".format(pattern, last_text[:1500])
    )


def snap(page: Page, filename: str, *, full_page: bool = True) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    page.wait_for_timeout(1500)
    page.screenshot(path=str(path), full_page=full_page)
    return str(path.relative_to(ROOT))


def record_case(
    summary: list[dict[str, object]],
    *,
    name: str,
    status: str,
    url: str,
    screenshot: str | None = None,
    notes: list[str] | None = None,
) -> None:
    summary.append(
        {
            "name": name,
            "status": status,
            "url": url,
            "screenshot": screenshot,
            "notes": notes or [],
        }
    )


def attach_listeners(
    page: Page,
    *,
    page_name: str,
    console_messages: list[dict[str, str]],
    page_errors: list[dict[str, str]],
    request_failures: list[dict[str, str]],
) -> None:
    page.on(
        "console",
        lambda msg: console_messages.append(
            {"page": page_name, "type": msg.type, "text": msg.text}
        ),
    )
    page.on(
        "pageerror",
        lambda exc: page_errors.append({"page": page_name, "text": str(exc)}),
    )
    page.on(
        "requestfailed",
        lambda req: request_failures.append(
            {
                "page": page_name,
                "method": req.method,
                "url": req.url,
                "error": req.failure.error_text if req.failure else "unknown",
            }
        ),
    )


def main() -> None:
    summary: list[dict[str, object]] = []
    console_messages: list[dict[str, str]] = []
    page_errors: list[dict[str, str]] = []
    request_failures: list[dict[str, str]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1600})

        page = context.new_page()
        attach_listeners(
            page,
            page_name="main-flow",
            console_messages=console_messages,
            page_errors=page_errors,
            request_failures=request_failures,
        )

        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60_000)
        wait_for_body_contains(page, ["Sign In", "View Demo"])
        landing_url = wait_for_route(page, "landing")
        record_case(
            summary,
            name="landing",
            status="pass",
            url=landing_url,
            screenshot=snap(page, "01-landing.png"),
            notes=["Landing controls rendered and URL normalized to route=landing."],
        )

        page.get_by_role("button", name="Sign In").first.click()
        wait_for_body_contains(page, ["Coordinator Demo Login", "Volunteer (Coming Soon)"])
        login_url = wait_for_route(page, "login")
        record_case(
            summary,
            name="login",
            status="pass",
            url=login_url,
            screenshot=snap(page, "02-login.png"),
            notes=["Landing Sign In routed to the login page."],
        )

        page.get_by_role("button", name="< Back to Home").first.click()
        wait_for_body_contains(page, ["Sign In", "View Demo"])
        page.get_by_role("button", name="View Demo").first.click()
        wait_for_body_contains(
            page,
            ["Dashboard", "Matches", "Discovery", "Show Jarvis Command Center", "View Match Engine"],
        )
        demo_url = wait_for_route(page, "dashboard")
        record_case(
            summary,
            name="view_demo",
            status="pass",
            url=demo_url,
            screenshot=snap(page, "03-view-demo-dashboard.png"),
            notes=["View Demo routed directly into the dashboard with demo mode enabled."],
        )

        workspace_expectations = [
            ("dashboard", None, ["Show Jarvis Command Center", "Campus Coverage Map"]),
            ("matches", "Matches", ["Matches", "Select an Event"]),
            ("discovery", "Discovery", ["University Event Discovery"]),
            ("pipeline", "Pipeline", ["Engagement Pipeline"]),
            (
                "analytics",
                "Analytics",
                ["Analytics", "Coverage, expansion readiness, and volunteer engagement analytics."],
            ),
            (
                "match_engine",
                "Match Engine",
                ["Match workspace is embedded below.", "< Back to Dashboard", "Sign Out"],
            ),
        ]

        for index, (route_name, button_name, expected_text) in enumerate(
            workspace_expectations,
            start=4,
        ):
            if button_name:
                page.get_by_role("button", name=button_name).first.click()
            wait_for_body_contains(page, expected_text)
            current_url = wait_for_route(page, route_name)
            notes = [f"Workspace nav reached {route_name}."]
            if route_name == "analytics":
                notes.append("Analytics page exposed the routed expansion and volunteer analytics surface.")
            if route_name == "match_engine":
                notes.append("Match Engine rendered the new caption above the embedded workspace.")
            record_case(
                summary,
                name=f"workspace_{route_name}",
                status="pass",
                url=current_url,
                screenshot=snap(page, f"{index:02d}-workspace-{route_name}.png"),
                notes=notes,
            )

        page.get_by_role("button", name="Dashboard").first.click()
        wait_for_body_contains(page, ["Show Jarvis Command Center", "Campus Coverage Map"])
        wait_for_route(page, "dashboard")

        page.locator(
            "label[data-baseweb='checkbox']",
            has_text="Show Jarvis Command Center",
        ).first.click(timeout=10_000)
        wait_for_body_contains(page, ["Jarvis -- Voice Command Center", "Send Command"])
        record_case(
            summary,
            name="jarvis_toggle",
            status="pass",
            url=page.url,
            screenshot=snap(page, "10-jarvis-open.png"),
            notes=["Jarvis checkbox opened the command center above the dashboard iframe."],
        )

        page.get_by_role("textbox", name="Command").fill("Find new events")
        page.get_by_role("button", name="Send Command").click()
        wait_for_body_contains(page, ["Scrape universities for new events", "Approve", "Reject"])
        record_case(
            summary,
            name="jarvis_text_command",
            status="pass",
            url=page.url,
            screenshot=snap(page, "11-jarvis-proposal.png"),
            notes=["Text command produced a Discovery Agent proposal with Approve/Reject controls."],
        )

        page.get_by_role("button", name="Approve").last.click()
        result_text = wait_for_regex(page, r"Found \d+ event\(s\) \(source: [^)]+\)")
        record_case(
            summary,
            name="jarvis_execution",
            status="pass",
            url=page.url,
            screenshot=snap(page, "12-jarvis-execution.png"),
            notes=[f"Approved discovery action completed through the UI: {result_text}."],
        )

        page.get_by_role("button", name="Sign Out").first.click()
        wait_for_body_contains(page, ["Sign In", "View Demo"])
        signout_url = wait_for_route(page, "landing")
        record_case(
            summary,
            name="sign_out",
            status="pass",
            url=signout_url,
            screenshot=snap(page, "13-sign-out.png"),
            notes=["Workspace Sign Out returned to landing and cleared demo routing."],
        )

        deep_links = [
            (
                "deep_link_matches",
                f"{BASE_URL}/?route=matches",
                "matches",
                ["Matches", "Select an Event"],
                "14-deep-link-matches.png",
                "Direct matches link rendered the Matches workspace.",
            ),
            (
                "deep_link_coordinator",
                f"{BASE_URL}/?route=coordinator&demo=1",
                "dashboard",
                ["Show Jarvis Command Center", "Campus Coverage Map"],
                "15-deep-link-coordinator.png",
                "Coordinator alias normalized to dashboard while preserving demo=1.",
            ),
            (
                "deep_link_unknown",
                f"{BASE_URL}/?route=unknown",
                "landing",
                ["Sign In", "View Demo"],
                "16-deep-link-unknown.png",
                "Unknown route normalized back to landing.",
            ),
        ]

        for name, url, route_name, expected_text, filename, note in deep_links:
            subpage = context.new_page()
            attach_listeners(
                subpage,
                page_name=name,
                console_messages=console_messages,
                page_errors=page_errors,
                request_failures=request_failures,
            )
            subpage.goto(url, wait_until="domcontentloaded", timeout=60_000)
            wait_for_body_contains(subpage, expected_text)
            final_url = wait_for_route(subpage, route_name)
            record_case(
                summary,
                name=name,
                status="pass",
                url=final_url,
                screenshot=snap(subpage, filename),
                notes=[note],
            )
            subpage.close()

        browser.close()

    unique_console: list[dict[str, str]] = []
    seen_console: set[tuple[str, str]] = set()
    for entry in console_messages:
        if entry["type"] not in {"warning", "error"}:
            continue
        key = (entry["type"], entry["text"])
        if key in seen_console:
            continue
        seen_console.add(key)
        unique_console.append(entry)

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "base_url": BASE_URL,
        "summary": summary,
        "console": unique_console,
        "page_errors": page_errors,
        "request_failures": request_failures,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "summary_path": str(SUMMARY_PATH),
                "cases": len(summary),
                "warnings": len(unique_console),
                "page_errors": len(page_errors),
                "request_failures": len(request_failures),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
