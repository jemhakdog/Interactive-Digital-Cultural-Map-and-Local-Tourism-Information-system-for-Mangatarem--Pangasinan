# Schemas Module Contract (`backend/app/schemas`)

## Overview
The `backend.app.schemas` package defines Pydantic models enforcing structural typing, payload validation, and outbound JSON serialization schemas for all HTTP endpoints.

## Interface
- `auth`: `LoginRequest`, `RegisterRequest`, `TokenResponse`, `UserResponse`, `RefreshRequest`, `ForgotPasswordRequest`, `ResetPasswordRequest`, `GoogleAuthRequest`, `UserRole`.
- `attraction`: `AttractionCreate`, `AttractionUpdate`, `AttractionResponse`, `AttractionListResponse`, `ReviewCreate`, `ReviewResponse`, `ReviewListResponse`.
- `booking`: `AvailabilityResponse`, `ReserveRequest`, `ReserveResponse`, `VerifyArrivalRequest`, `VerifyArrivalResponse`.
- `business`: `EstablishmentCreate`, `EstablishmentUpdate`, `EstablishmentResponse`, `EstablishmentListResponse`.
- `chat`: `ChatMessageResponse`, `ChatRoomResponse`, `SendMessageRequest`, `SendMessageResponse`.
- `document`: `DocumentCreate`, `DocumentResponse`.
- `event`: `EventCreate`, `EventUpdate`, `EventResponse`, `EventListResponse`.
- `gamification`: `CheckinRequest`, `CheckinResponse`, `CheckinBadgeResponse`, `StartNavigationRequest`.
- `heritage`: `HeritageProfileCreate`, `HeritageProfileUpdate`, `HeritageProfileResponse`, `HeritageListResponse`.
- `notification` & `newsletter`: `SubscribeRequest`, `NewsletterSend`, `NotificationItem`, `NotificationListResponse`.
- `user` & `visitor`: `UserProfileResponse`, `VisitorRegistryResponse`, `VisitorLogRequest`.

## Invariants
- All incoming payload attributes are validated before execution reaches route controllers; violations raise HTTP 422 automatically.
- Outbound schemas exclude sensitive internal fields like `password_hash` and raw password reset tokens.

## Side Effects
- Pure computation and data parsing; no network or storage side effects.

## Verification
- Run: `.venv/bin/pytest tests/`
