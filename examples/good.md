# Set up authentication

Generate an API token from the Settings page and add it to your configuration file.

## Prerequisites

Before you start, verify that your account has admin permissions.

## Configure the client

1. Open the `config.yml` file in your project root.
2. Add your API token to the `auth.token` field.
3. Set `auth.enabled` to `true`.

```yaml
auth:
  enabled: true
  token: "your-api-token-here"
```

## Verify your connection

Run the health check command to confirm the client connects to the API:

```bash
docs-cli health --verbose
```

A successful response includes a `status: ok` field and your account ID.

## Rate limits

The API enforces a limit of 100 requests per minute per token.
If you exceed the limit, the server returns a `429 Too Many Requests` response.
Wait for the retry window (indicated in the `Retry-After` header) before sending another request.

## Next steps

- Review the API reference for available endpoints.
- Configure webhook notifications for real-time updates.
- Set up a CI/CD pipeline to automate documentation checks.
