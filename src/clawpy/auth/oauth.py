"""OAuth 2.0 PKCE flow for Claude subscription authentication.

Mimics Claude Code's OAuth flow to authenticate with a Claude.ai subscription.
Uses the same client ID, scopes, and endpoints as Claude Code.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import secrets
import time
import webbrowser
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx

from clawpy.config.paths import global_config_dir

# ---- OAuth Constants (from OpenClaude src/constants/oauth.ts) ----

CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
AUTHORIZE_URL = "https://claude.ai/oauth/authorize"
TOKEN_URL = "https://platform.claude.com/v1/oauth/token"
PROFILE_URL = "https://api.anthropic.com/api/oauth/profile"
MANUAL_REDIRECT_URI = "https://platform.claude.com/oauth/code/callback"

SCOPES = [
    "user:profile",
    "user:inference",
    "user:sessions:claude_code",
    "user:mcp_servers",
    "user:file_upload",
    "org:create_api_key",
]

CREDENTIALS_FILE = "credentials.json"


@dataclass(slots=True)
class OAuthTokens:
    """Stored OAuth tokens."""

    access_token: str
    refresh_token: str
    expires_at: float  # Unix timestamp
    scopes: list[str]
    account_uuid: str = ""
    email: str = ""
    organization_uuid: str = ""

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.expires_at - 300  # 5 min buffer

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OAuthTokens:
        return cls(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=data["expires_at"],
            scopes=data.get("scopes", SCOPES),
            account_uuid=data.get("account_uuid", ""),
            email=data.get("email", ""),
            organization_uuid=data.get("organization_uuid", ""),
        )


def _credentials_path() -> Path:
    return global_config_dir() / CREDENTIALS_FILE


def load_tokens() -> OAuthTokens | None:
    """Load stored OAuth tokens, or None if not logged in."""
    path = _credentials_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return OAuthTokens.from_dict(data)
    except (json.JSONDecodeError, KeyError):
        return None


def save_tokens(tokens: OAuthTokens) -> None:
    """Save OAuth tokens to disk."""
    path = _credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tokens.to_dict(), indent=2))
    # Restrict permissions
    os.chmod(path, 0o600)


def is_logged_in() -> bool:
    """Check if we have stored (possibly expired) OAuth tokens."""
    return load_tokens() is not None


def clear_tokens() -> None:
    """Remove stored tokens (logout)."""
    path = _credentials_path()
    if path.exists():
        path.unlink()


# ---- PKCE helpers ----

def _generate_code_verifier() -> str:
    """32 random bytes, base64url-encoded (no padding)."""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()


def _generate_code_challenge(verifier: str) -> str:
    """SHA-256 of verifier, base64url-encoded (no padding)."""
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def _generate_state() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()


# ---- Callback server ----

class _CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures the OAuth callback."""

    auth_code: str | None = None
    state: str | None = None
    error: str | None = None

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "error" in params:
            _CallbackHandler.error = params["error"][0]
            self._respond("Authentication failed. You can close this tab.")
            return

        _CallbackHandler.auth_code = params.get("code", [None])[0]
        _CallbackHandler.state = params.get("state", [None])[0]
        self._respond(
            "Authentication successful! You can close this tab and return to ClawPy."
        )

    def _respond(self, message: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html = f"""<html><body style="font-family:sans-serif;text-align:center;padding:50px">
        <h2>{message}</h2></body></html>"""
        self.wfile.write(html.encode())

    def log_message(self, format: str, *args: Any) -> None:
        pass  # Suppress server logs


class OAuthFlow:
    """Manages the complete OAuth PKCE login flow."""

    def __init__(self) -> None:
        self._verifier = _generate_code_verifier()
        self._challenge = _generate_code_challenge(self._verifier)
        self._state = _generate_state()

    async def login(self, manual: bool = False) -> OAuthTokens:
        """Run the full OAuth login flow.

        Args:
            manual: If True, print the URL for manual copy instead of auto-opening browser.

        Returns:
            OAuthTokens on success.

        Raises:
            RuntimeError on failure.
        """
        if manual:
            return await self._manual_flow()
        return await self._auto_flow()

    async def _auto_flow(self) -> OAuthTokens:
        """Auto flow: start local server, open browser, wait for callback."""
        # Start callback server on random port
        server = HTTPServer(("127.0.0.1", 0), _CallbackHandler)
        port = server.server_address[1]
        redirect_uri = f"http://localhost:{port}/callback"

        thread = Thread(target=server.handle_request, daemon=True)
        thread.start()

        # Build authorize URL
        auth_url = self._build_authorize_url(redirect_uri)
        print(f"\nOpening browser for authentication...")
        print(f"If it doesn't open, visit:\n{auth_url}\n")
        webbrowser.open(auth_url)

        # Wait for callback (timeout 120s)
        thread.join(timeout=120)
        server.server_close()

        if _CallbackHandler.error:
            raise RuntimeError(f"OAuth error: {_CallbackHandler.error}")
        if not _CallbackHandler.auth_code:
            raise RuntimeError("No authorization code received (timeout?)")
        if _CallbackHandler.state != self._state:
            raise RuntimeError("State mismatch — possible CSRF attack")

        # Exchange code for tokens
        tokens = await self._exchange_code(
            _CallbackHandler.auth_code, redirect_uri
        )

        # Fetch profile
        tokens = await self._fetch_profile(tokens)

        # Save
        save_tokens(tokens)
        return tokens

    async def _manual_flow(self) -> OAuthTokens:
        """Manual flow: user copies URL, pastes code back."""
        redirect_uri = MANUAL_REDIRECT_URI
        auth_url = self._build_authorize_url(redirect_uri)

        print(f"\nOpen this URL in your browser:\n")
        print(auth_url)
        print(f"\nAfter authorizing, you'll be redirected to a page with a code.")
        print("(Paste the full URL or just the code)")
        raw = input("Code: ").strip()

        if not raw:
            raise RuntimeError("No code provided")

        # The callback page may give "CODE#STATE" or a full URL with ?code=...
        code = raw
        if "#" in code:
            code = code.split("#")[0]
        if "code=" in code:
            from urllib.parse import parse_qs, urlparse
            parsed = urlparse(code)
            params = parse_qs(parsed.query) if parsed.query else parse_qs(parsed.path)
            code = params.get("code", [code])[0]

        tokens = await self._exchange_code(code, redirect_uri)
        tokens = await self._fetch_profile(tokens)
        save_tokens(tokens)
        return tokens

    def _build_authorize_url(self, redirect_uri: str) -> str:
        params = {
            "code": "true",
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(SCOPES),
            "code_challenge": self._challenge,
            "code_challenge_method": "S256",
            "state": self._state,
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    async def _exchange_code(
        self, code: str, redirect_uri: str
    ) -> OAuthTokens:
        """Exchange authorization code for access + refresh tokens."""
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                TOKEN_URL,
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": CLIENT_ID,
                    "code_verifier": self._verifier,
                    "state": self._state,
                },
            )
            if resp.status_code != 200:
                raise RuntimeError(
                    f"Token exchange failed ({resp.status_code}): {resp.text}"
                )

            data = resp.json()

        expires_in = data.get("expires_in", 3600)
        account = data.get("account", {})

        return OAuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", ""),
            expires_at=time.time() + expires_in,
            scopes=data.get("scope", " ".join(SCOPES)).split(),
            account_uuid=account.get("uuid", ""),
            email=account.get("email", ""),
            organization_uuid=data.get("organization", {}).get("uuid", ""),
        )

    async def _fetch_profile(self, tokens: OAuthTokens) -> OAuthTokens:
        """Fetch user profile to get subscription info."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    PROFILE_URL,
                    headers={"Authorization": f"Bearer {tokens.access_token}"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    tokens.email = data.get("email", tokens.email)
                    tokens.account_uuid = data.get("account_uuid", tokens.account_uuid)
        except Exception:
            pass  # Profile fetch is best-effort
        return tokens


async def refresh_tokens(tokens: OAuthTokens) -> OAuthTokens:
    """Refresh expired tokens."""
    # Use inference-only scopes for refresh (org:create_api_key is console-only)
    refresh_scopes = [s for s in tokens.scopes if s != "org:create_api_key"]
    if not refresh_scopes:
        refresh_scopes = ["user:profile", "user:inference"]

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            TOKEN_URL,
            json={
                "grant_type": "refresh_token",
                "refresh_token": tokens.refresh_token,
                "client_id": CLIENT_ID,
                "scope": " ".join(refresh_scopes),
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Token refresh failed ({resp.status_code}): {resp.text}. "
                "Run 'clawpy login' to re-authenticate."
            )

        data = resp.json()

    expires_in = data.get("expires_in", 3600)
    account = data.get("account", {})

    refreshed = OAuthTokens(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token", tokens.refresh_token),
        expires_at=time.time() + expires_in,
        scopes=data.get("scope", " ".join(tokens.scopes)).split()
            if isinstance(data.get("scope"), str)
            else tokens.scopes,
        account_uuid=account.get("uuid", tokens.account_uuid),
        email=account.get("email", tokens.email),
        organization_uuid=data.get("organization", {}).get("uuid", tokens.organization_uuid),
    )
    save_tokens(refreshed)
    return refreshed
