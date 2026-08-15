# OAuth Authentication Notes

## Required Headers for Claude Subscription

When authenticating via OAuth (Claude Pro/Max/Team/Enterprise subscription), the Anthropic API requires specific headers beyond just `Authorization: Bearer <token>`. Without these, the API returns `429 "Error"` (not a real rate limit).

### Critical Headers

| Header | Value | Why |
|--------|-------|-----|
| `Authorization` | `Bearer <oauth_token>` | OAuth token (not API key) |
| `anthropic-beta` | Must include `oauth-2025-04-20` | Tells API to accept OAuth auth |
| `anthropic-beta` | Must include `claude-code-20250219` | Identifies as Claude Code client |
| `x-app` | `cli` | Application identifier |
| `User-Agent` | `claude-cli/<version> (external, cli)` | Client identification |
| `x-client-request-id` | UUID per request | Request tracking |

### System Prompt Billing Attribution

The first system prompt block must be the billing header:
```
x-anthropic-billing-header: cc_version=<version>; cc_entrypoint=cli; cch=00000;
```

The `cch=00000` is a client attestation hash. In real Claude Code, this is computed by Bun's HTTP layer. For third-party clients, `00000` is accepted.

### Request Body Metadata

OAuth requests must include:
```json
{
  "metadata": {
    "user_id": "{\"account_uuid\": \"<uuid>\", \"session_id\": \"<uuid>\"}"
  }
}
```

### What Happens Without These

| Missing | Error |
|---------|-------|
| `oauth-2025-04-20` beta | 401 "OAuth authentication is currently not supported" |
| `claude-code-20250219` beta | 429 "Error" (fake rate limit) |
| Billing attribution | 429 "Error" (fake rate limit) |
| `metadata.user_id` | May work but billing may not route correctly |

### Future Considerations

- Beta header strings may change — check OpenClaude's `src/utils/betas.ts` if auth stops working
- The `cch` attestation may become enforced — would need to reverse-engineer the hash
- Token refresh uses the same OAuth endpoint with `grant_type=refresh_token`
- Scopes may expand — Claude Code now requests `user:file_upload` and `user:mcp_servers`
