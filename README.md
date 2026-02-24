# OAuth Learning Lab: Authentication Server Prototype

This repository houses an experimental, learning-focused implementation of an **OAuth 2.0 Authorization Server** and **Resource Server**, designed to explore advanced identity patterns, particularly **Proof Key for Code Exchange (PKCE)** and **Client-ID Metadata Documents (CIMD)**.

## Overview

The purpose of this prototype is to deeply understand the mechanics of OAuth 2.0 Authorization Code flows, decentralized client registration via CIMD, and securing token exchange mechanisms. It is intentionally minimal, isolating the core protocol flows from complex identity provider features like user authentication or persistent storage.

## Key Features

- **Authorization Code Flow with PKCE**: Mandates the use of PKCE (`S256` challenge method) to prevent authorization code interception attacks.
- **Client-ID Metadata Document (CIMD)**: Implements decentralized, dynamic client registration inspired by OpenID Federation and IndieAuth. The `client_id` acts as a securely hosted URL containing the client's metadata (e.g., allowed redirect URIs, supported grant types).
- **Opaque Access Tokens**: Issues cryptographically secure random opaque tokens for protected resource access.
- **Resource Server Validation**: Includes a mock resource server (`/resource/research`) that strictly validates bearer tokens and required scopes against the authorization server's state.

## System Architecture

1. **Authorization Endpoint (`/authorize`)**:
   - Initiates the OAuth flow.
   - Fetches and caches the CIMD using the provided `client_id` (treated as a URL).
   - Validates the `redirect_uri` against the client's registered metadata document.
   - Issues a one-time-use authorization code.
2. **Token Endpoint (`/token`)**:
   - Validates the authorization code and original bindings (`client_id`, `redirect_uri`).
   - Verifies the PKCE `code_verifier` against the previously stored `code_challenge`.
   - Issues an Access Token and binds the authorized scopes.
3. **Resource Endpoint (`/resource/research`)**:
   - Expects an `Authorization: Bearer <token>` header.
   - Validates the token's existence and enforces the `"research.read"` scope.

## Getting Started

### Prerequisites

- Python >= 3.13
- `uv` package manager

### Installation

Install dependencies and set up the environment:

```bash
uv sync
```

### Running the Application

The application is built with FastAPI. Start the development server using the project's custom script:

```bash
uv run app
```

Alternatively, you can run it directly via Uvicorn:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Security & Production Gaps

**⚠️ Warning: This is a learning prototype and is NOT production-ready.**

While the prototype implements advanced flow concepts, it contains deliberate simplifications:

- **In-Memory Storage**: Relies on volatile Python dictionaries for state management (`AUTHORIZATION_CODES`, `ACCESS_TOKENS`, CIMD cache). This means total data loss on server restarts and an inability to scale horizontally across multiple instances.
- **No User Authentication**: The `/authorize` endpoint automatically issues codes without requiring user authentication (login) or consent.
- **Immortal Tokens**: Although tokens are issued with an `expires_in` attribute, the token validation process omits expiration checks, leaving tokens active indefinitely in memory.
- **CSRF Assumptions**: The prototype relies completely on PKCE to prevent token interception but lacks proper `state` parameter validation to prevent CSRF.

For production environments requiring these advanced OAuth/OIDC capabilities, consider utilizing a robust identity architecture or an API-driven authorization engine like [Authlete](https://www.authlete.com/).
