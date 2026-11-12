---
title: "Nobody Tells You When a Refresh Token Expires"
description: "OAuth providers limit refresh tokens in very different ways, and an integrator can read these limits only in vendor documentation, if at all. An IETF draft would put them into the token response."
claim: "OAuth providers know when a refresh token will stop working, but no standard lets a client read that today, so every vendor documents its limits differently or invents its own response field."
lead: "The OAuth providers I integrated each had their own idea of how long a refresh token lives, and my client could rarely read it. An IETF draft wants to change that, and I think it is a good start that doesn't go far enough."
date: 2026-11-12T19:51:11+01:00
slug: refresh-token-lifetime
tags: ["oauth2"]
findings:
  - id: refresh-token-limits-undiscoverable
    text: "In vendor documentation read on 12 November 2026, 18 OAuth providers limit refresh tokens anywhere between 24 hours (Microsoft, for single-page apps) and 5 years (Intuit). At 6 of the 18, whoever operates the tenant sets the limit, and only 4 report it in the token response."
  - id: refresh-token-vendor-fields
    text: "GitHub, Airtable, Keycloak and Intuit each return the remaining refresh token lifetime in the token response under their own field names: refresh_token_expires_in at GitHub, refresh_expires_in at Airtable and Keycloak, and x_refresh_token_expires_in at Intuit."
  - id: refresh-token-expiration-draft
    text: "The IETF draft draft-ietf-oauth-refresh-token-expiration-03 from July 2026 adds refresh_token_timeout and authorization_expires_in to the token response. It keeps invalid_grant as the only error and has an intended status of Informational."
---

While integrating third-party OAuth providers into the [Agentic Identity Broker]({{< ref "/projects/agentic-identity-broker" >}}) (AIB) I co-authored, three things cost me the most. Refresh tokens expired without any announcement. When they did, the provider answered with the same `invalid_grant` it uses for every other cause. And some providers let an administrator change how refresh tokens rotate, with unclear side effects on token issuing and expiry.

All three come down to the same gap. A provider knows when a refresh token will stop working, and OAuth gives it no standard way to tell the client. So each vendor writes its limits into its documentation, or returns them in a field it made up, or says nothing. I don't blame the vendors for having different limits. What I'd ask for is that a client can read them. An IETF draft proposes that, and below I go through what providers do today, what the draft adds and what I still miss in it.

## Why providers pick their own limits

The specifications leave refresh token lifetimes open. The draft I discuss below sums up RFC 6749 like this: OAuth 2.0 "does not contain any normative language around expiration or lack thereof for refresh tokens, mentioning only that they are 'typically long-lasting'". The security best practice, [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700#section-4.14.2 "RFC 9700, Section 4.14.2: Recommendations"), says that refresh tokens "SHOULD expire if the client has been inactive for some time" and puts the expiration time "at the discretion of the authorization server".

I have built OAuth and OpenID Connect providers myself, and in my experience the refresh token lifetime is often tied to how the provider models its login session. Keycloak shows that openly. Its [administration guide](https://www.keycloak.org/docs/latest/server_admin/#_refresh_token_grant "Keycloak Server Administration Guide: Refresh token grant") says a refresh token "is tied to the user session of the SSO browser session", and the two settings that bound it are called SSO Session Idle and SSO Session Max. A team that tunes those two for its login experience has also decided how long every integration stays connected.

So an idle limit and an absolute limit are reasonable things for a provider to have. The trouble starts on the integrator's side, where I have to find each provider's combination and hard-code it.

## What 18 providers document

To see how far the limits spread, I had my agent read the OAuth documentation of 18 providers on 12 November 2026. The table lists what each vendor documents. "Renewed by refreshing" means that a successful refresh starts the clock again, and "tenant" means that whoever operates or administers the tenant sets the limit.

| Provider | Refresh token limit | Renewed by refreshing | Set by | In the token response |
|---|---|---|---|---|
| [Airtable](https://airtable.com/developers/web/api/oauth-reference "Airtable: OAuth reference") | 60 days | yes | vendor | `refresh_expires_in` |
| [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-refresh-token.html "Amazon Cognito: Refresh tokens") | 30 days after sign-in by default, 60 minutes to 10 years | no | tenant | no |
| [Atlassian](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/ "Atlassian: OAuth 2.0 (3LO) apps") | 90 days of inactivity | yes | vendor | no |
| [Auth0](https://auth0.com/docs/secure/tokens/refresh-tokens/configure-refresh-token-expiration "Auth0: Configure refresh token expiration") | idle 30 days by default, maximum up to 1 year | idle yes, maximum no | tenant | no |
| [Box](https://developer.box.com/guides/authentication/tokens/refresh/ "Box: Refresh a token") | 60 days | yes | vendor | no |
| [Databricks](https://docs.databricks.com/api/o-auth/v1/custom-app-integration "Databricks API: Custom App Integration") | 7 days by default, 5 minutes to 90 days | only with single-use tokens | tenant | no |
| [GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens "GitHub: Refreshing user access tokens") | 6 months | yes | vendor | `refresh_token_expires_in` |
| [Google](https://developers.google.com/identity/protocols/oauth2#expiration "Google: Refresh token expiration") | 6 months without use | yes | vendor, or the user with time-based access | no |
| [Intuit QuickBooks](https://blogs.intuit.com/2025/11/12/important-changes-to-refresh-token-policy "Intuit: Important changes to refresh token policy") | 100 days without use, 5 years in total | 100 days yes, 5 years no | vendor | `x_refresh_token_expires_in` |
| [Keycloak](https://www.keycloak.org/docs/latest/server_admin/#_timeouts "Keycloak Server Administration Guide: Timeouts") | session idle and session maximum | idle yes, maximum no | tenant | `refresh_expires_in` |
| [Linear](https://linear.app/developers/oauth-2-0-authentication "Linear: OAuth 2.0 authentication") | 30 days | yes | vendor | no |
| [Microsoft Entra](https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens "Microsoft: Refresh tokens in the Microsoft identity platform") | 90 days by default, 24 hours for single-page apps | not for single-page apps | vendor | no |
| [Notion MCP](https://developers.notion.com/guides/mcp/build-mcp-client "Notion: Build an MCP client") | 180 days from authorization | no | vendor | no |
| [Okta](https://developer.okta.com/docs/guides/refresh-tokens/main/ "Okta: Refresh access tokens and rotate refresh tokens") | unlimited by default, 7 days without use | idle yes | tenant | no |
| [Salesforce](https://help.salesforce.com/s/articleView?id=xcloud.connected_app_manage_oauth.htm&type=5 "Salesforce: Manage OAuth access policies for a connected app") | until revoked by default, or idle, or fixed | depends on the policy | tenant | no |
| [Spotify](https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens "Spotify: Refreshing tokens") | 6 months from authorization | no | vendor | no |
| [Xero](https://developer.xero.com/faq/oauth2 "Xero: OAuth 2.0 FAQs") | 60 days without use | yes | vendor | no |
| [Zoom](https://developers.zoom.us/docs/integrations/oauth/ "Zoom: OAuth") | 90 days | not stated | vendor | no |

A "no" in the last column means that the linked documentation shows no such field. The table rests on documentation alone and not on tests, so please read it as a snapshot of vendor claims.

The documented limits go from 24 hours for single-page apps at Microsoft to 5 years at Intuit, and the default at Salesforce has no limit at all. The numbers also mean different things. At Linear or Box, a client that refreshes regularly keeps its connection for good. At Notion or Spotify, the same client loses it after 180 days or 6 months, however often it refreshed. At 6 of the 18, the vendor doesn't decide the limit. Auth0, Cognito, Keycloak and Okta are identity products that other companies run, and at Databricks and Salesforce the customer's administrator configures the policy per application. For these 6, the documentation only gives me the range of what I might meet.

## Rotation settings change the rules per tenant

Databricks is the example I ran into myself. An account administrator can set a refresh token time-to-live (TTL) for each OAuth application, 7 days by default, and can turn on single-use refresh tokens, which is Databricks' name for refresh token rotation. The [API reference](https://docs.databricks.com/api/o-auth/v1/custom-app-integration "Databricks API: Custom App Integration") explains what that switch does to the first setting: "When single-use refresh tokens are enabled, this represents the TTL of an individual refresh token. If the refresh token is used before it expires, a new one is issued with a renewed individual TTL." A second setting, the absolute session lifetime, is "effective only when the single-use refresh token feature is enabled".

So with rotation on, the same number becomes a sliding limit, and the session gets an absolute end that doesn't exist with rotation off. According to the [Databricks documentation](https://docs.databricks.com/aws/en/integrations/single-use-tokens "Databricks: Single-use refresh tokens"), rotation is on by default for three published applications and has to be enabled through the API for most others. My client sees none of this. It gets a refresh token and finds out later which combination the administrator chose.

Rotation also comes with a window in which the previous refresh token still works, so that a lost response doesn't end the session. Every vendor sizes it differently: Okta 30 seconds by default, Atlassian 10 minutes, Linear and Xero 30 minutes, and Notion keeps the one previous token valid. Outside that window, Notion treats a reused token as stolen and can revoke the whole grant. A client that runs more than one replica has to know these numbers, and they exist in documentation only as well.

## One error for every cause

When a refresh token has ended, the client learns it through `invalid_grant`. [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749#section-5.2 "RFC 6749, Section 5.2: Error Response") defines that code for a grant or refresh token that "is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client". The vendors add their own causes behind it. Atlassian returns it after the user changed their password. Microsoft documents a matrix of which password event revokes which kind of refresh token. Google invalidates the oldest token "without warning" once an account holds more than 100 for the same client.

I can't tell these causes apart in the client, so I can't tell the user either. "Your access expired after 90 days" and "someone revoked this app" call for different messages, and my client only knows that the person has to log in again. Google is an exception for one case: when an administrator's session policy ends the access, it adds an `error_subtype` to the response. In case you want to read more about the revocation side, see my field guide entry on [consent and revocation]({{< ref "/knowledge-base/agent-identity/consent-and-revocation" >}} "How should people grant and revoke an agent's access?").

## Four vendors, four field names

A few vendors noticed the gap and closed it for themselves.

| Vendor | Field in the token response | Meaning |
|---|---|---|
| GitHub | `refresh_token_expires_in` | seconds until the refresh token expires, always 6 months |
| Airtable | `refresh_expires_in` | seconds until the refresh token expires, 60 days expected |
| Keycloak | `refresh_expires_in` | refresh token expiry, per its [token response class](https://github.com/keycloak/keycloak/blob/main/core/src/main/java/org/keycloak/representations/AccessTokenResponse.java "Keycloak: AccessTokenResponse.java") |
| Intuit | `x_refresh_token_expires_in` | seconds left of the rolling 100 days |
| Intuit | `x_refresh_token_hard_expires_in` | seconds left of the 5 years, only on request |

Intuit shows what a known date makes possible. In November 2025, it [announced](https://blogs.intuit.com/2025/11/12/important-changes-to-refresh-token-policy "Intuit: Important changes to refresh token policy") that refresh tokens, which had been "effectively permanent" as long as a client used them every 100 days, now end after 5 years. Along with the second field, it promised to remind QuickBooks customers 30 days and again 7 days before a connection expires. For me as an integrator, the downside is that planning ahead currently needs a code path per vendor.

## What the IETF draft adds

[OAuth 2.0 Refresh Token and Authorization Expiration](https://datatracker.ietf.org/doc/draft-ietf-oauth-refresh-token-expiration/ "draft-ietf-oauth-refresh-token-expiration") by Nick Watson of Google started as an individual draft in June 2025. The OAuth working group adopted it in December 2025, and revision 03 is from 6 July 2026. It defines two parameters for the token response:

- `refresh_token_timeout` is the "time in seconds that the refresh token may be held by the client without exchanging", which is the idle limit.
- `authorization_expires_in` is the "lifetime in seconds of the user's authorization for the scopes contained in the issued or presented refresh token", which is the absolute limit.

A provider with a 7-day idle limit and a user who granted access for 10 days would answer like this:

```json {filename="token-response.json"}
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "refresh_token_timeout": 604800,
  "authorization_expires_in": 864000
}
```

The two parameters match the two clocks from the table above. Linear could send only the first, Spotify only the second and Intuit both. An authorization server can announce its support in its metadata with `refresh_token_expiration_types_supported`, and the draft extends token introspection so that a client can ask about a refresh token it already holds. For rotating tokens, the draft says that the duration can now "be communicated as part of the API rather than relying on documentation".

## What I still miss in the draft

I consider the draft a good start, but it leaves three things open.

The error stays as it is. According to the draft, the "existing invalid_grant error code already explicitly covers token expiration and should be sufficient". For a planned expiry I agree, because the client knew the date. For every other cause, the client is where it was. I'd like to see a machine-readable reason next to `invalid_grant`, along the lines of Google's `error_subtype`, that separates expired, revoked and rotated-out tokens.

Rotation settings are missing too. Whether refresh tokens rotate and how long the previous one stays valid could be two more fields in the authorization server metadata. For a client with several replicas, they matter as much as the lifetime.

My biggest doubt is about adoption. The draft's intended status is Informational, and its metadata field is optional. GitHub, Airtable, Keycloak and Intuit already ship field names that their clients depend on, and an informational document doesn't oblige them to add a second set. As a Standards Track document, it would at least let profiles such as the MCP Authorization specification require the parameters.

## What an integrator can do today

Until providers report their limits, the limits have to live in the client. This is what I'd do in an integration today, and the vendor documentation backs most of it:

- Treat `invalid_grant` as final. Notion and Spotify both tell clients to discard the refresh token and start a new authorization instead of retrying.
- Allow only one refresh per grant at a time, across all replicas, and store the new refresh token together with the new access token before using either.
- Read the vendor's own expiry field where one exists, and read it from every response, because the value can change from one refresh to the next.
- Refresh connections that nobody uses before a known idle limit ends them.
- Keep the limits in configuration per provider and per tenant. With admin-set policies, two customers of the same vendor can behave differently.
- Tell the user the date where there is one, so they can reconnect before a job fails.

For MCP servers, I collect what vendors state about refresh token rotation in the [MCP auth atlas](https://letsauth.eu/mcp/ "MCP auth atlas") of Letsauth Lab, which I maintain. If you know how a provider expires or rotates its refresh tokens and the table above has it wrong, I'd like to hear about it.
