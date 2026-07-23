**Calendar scheduling, bookings, and availability for AI agents**

A Model Context Protocol (MCP) server that exposes Cal.com's v2 API for managing event types, bookings, schedules, availability, and organization membership.


## Overview

The MewCP Cal MCP Server provides programmatic access to a Cal.com scheduling account:

- Read and create event types, and inspect the authenticated user's profile
- Create, retrieve, reschedule, confirm, cancel, and mark bookings absent
- Manage availability schedules and query open time slots and busy times
- List organization memberships and routing forms

Perfect for:

- Automating meeting booking and rescheduling workflows
- Building scheduling assistants that surface open slots and busy times
- Managing team and organization scheduling resources programmatically


## Tools


### Profile


<details>
<summary><code>get_my_profile</code> — Get authenticated user profile from Cal.com</summary>

Get authenticated user profile from Cal.com

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  username?: string | null;
  email?: string | null;
  name?: string | null;
  timeZone?: string | null;
  weekStart?: string | null;
  locale?: string | null;
  timeFormat?: number | null;
  defaultScheduleId?: number | null;
  organizationId?: number | null;
  organization?: object | null;
  avatarUrl?: string | null;
  bio?: string | null;
  // additional upstream fields may be present
}
```

</details>


### Event Types


<details>
<summary><code>get_event_types</code> — List all event types for the user</summary>

List all event types for the user

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  event_types: {
    id?: number | null;
    title?: string | null;
    slug?: string | null;
    lengthInMinutes?: number | null;
    length?: number | null;
    description?: string | null;
    hidden?: boolean | null;
    ownerId?: number | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_event_type</code> — Get a specific event type by ID</summary>

Get a specific event type by ID

**Inputs:**
```
- `event_type_id` (integer, required) — The event type ID: the numeric Cal.com identifier of the event type to retrieve, as an integer (e.g. 123456). Required — the call fails with a validation error if omitted.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  title?: string | null;
  slug?: string | null;
  lengthInMinutes?: number | null;
  length?: number | null;
  description?: string | null;
  hidden?: boolean | null;
  ownerId?: number | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>create_event_type</code> — Create a new event type</summary>

Create a new event type

**Inputs:**
```
- `title` (string, required) — Title of the event type: the display name for the new event type, as a plain non-empty string (e.g. '30 Minute Meeting'). Required — the call fails with a validation error if omitted or blank.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  title?: string | null;
  slug?: string | null;
  lengthInMinutes?: number | null;
  length?: number | null;
  description?: string | null;
  hidden?: boolean | null;
  ownerId?: number | null;
  // additional upstream fields may be present
}
```

</details>


### Bookings


<details>
<summary><code>get_bookings</code> — Get all bookings for the user</summary>

Get all bookings for the user

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  bookings: {
    id?: number | null;
    uid?: string | null;
    title?: string | null;
    description?: string | null;
    status?: string | null;
    start?: string | null;
    end?: string | null;
    duration?: number | null;
    eventTypeId?: number | null;
    meetingUrl?: string | null;
    location?: string | null;
    absentHost?: boolean | null;
    cancellationReason?: string | null;
    rescheduledFromUid?: string | null;
    rescheduledToUid?: string | null;
    attendees?: {
      name?: string | null;
      email?: string | null;
      timeZone?: string | null;
      phoneNumber?: string | null;
      language?: string | null;
      absent?: boolean | null;
    }[] | null;
    hosts?: object[] | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_booking</code> — Get a specific booking by ID</summary>

Get a specific booking by ID

**Inputs:**
```
- `booking_id` (string, required) — The booking ID to retrieve, as a plain string (e.g. '12345'). Required.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  uid?: string | null;
  title?: string | null;
  description?: string | null;
  status?: string | null;
  start?: string | null;
  end?: string | null;
  duration?: number | null;
  eventTypeId?: number | null;
  meetingUrl?: string | null;
  location?: string | null;
  absentHost?: boolean | null;
  cancellationReason?: string | null;
  rescheduledFromUid?: string | null;
  rescheduledToUid?: string | null;
  attendees?: {
    name?: string | null;
    email?: string | null;
    timeZone?: string | null;
    phoneNumber?: string | null;
    language?: string | null;
    absent?: boolean | null;
  }[] | null;
  hosts?: object[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>create_booking</code> — Create a new booking</summary>

Create a new booking

**Inputs:**
```
- `event_type_id` (integer, required) — Event type ID to book, as an integer (e.g. 42). Required.
- `start` (string, required) — Booking start datetime in ISO 8601 / RFC 3339 UTC format (e.g. '2024-08-13T09:00:00Z'). Required.
- `attendee_name` (string, required) — Attendee full name as a plain string (e.g. 'Ada Lovelace'). Required.
- `attendee_email` (string, required) — Attendee email address as a plain string (e.g. 'ada@example.com'). Required.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  uid?: string | null;
  title?: string | null;
  description?: string | null;
  status?: string | null;
  start?: string | null;
  end?: string | null;
  duration?: number | null;
  eventTypeId?: number | null;
  meetingUrl?: string | null;
  location?: string | null;
  absentHost?: boolean | null;
  cancellationReason?: string | null;
  rescheduledFromUid?: string | null;
  rescheduledToUid?: string | null;
  attendees?: {
    name?: string | null;
    email?: string | null;
    timeZone?: string | null;
    phoneNumber?: string | null;
    language?: string | null;
    absent?: boolean | null;
  }[] | null;
  hosts?: object[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>cancel_booking</code> — Cancel a booking (DESTRUCTIVE, requires explicit user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Cancel a booking. Permanently cancels the booking identified by `booking_id`, releasing its time slot and notifying the host and every attendee. This action is irreversible — the cancelled booking and its confirmed slot cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly which booking will be cancelled and that it is permanent, and wait for their explicit written confirmation before proceeding. The response includes the booking's state before cancellation.

**Inputs:**
```
- `booking_id` (string, required) — The booking ID to cancel, as a plain string (e.g. '12345'). Required.
```

**Output `data` schema:**

```typescript
{
  before?: {
    id?: number | null;
    uid?: string | null;
    title?: string | null;
    description?: string | null;
    status?: string | null;
    start?: string | null;
    end?: string | null;
    duration?: number | null;
    eventTypeId?: number | null;
    meetingUrl?: string | null;
    location?: string | null;
    absentHost?: boolean | null;
    cancellationReason?: string | null;
    rescheduledFromUid?: string | null;
    rescheduledToUid?: string | null;
    attendees?: {
      name?: string | null;
      email?: string | null;
      timeZone?: string | null;
      phoneNumber?: string | null;
      language?: string | null;
      absent?: boolean | null;
    }[] | null;
    hosts?: object[] | null;
  } | null;
  after?: { /* same shape as `before` */ } | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>reschedule_booking</code> — Reschedule an existing booking</summary>

Reschedule an existing booking. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the current start and end times — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `booking_id` (string, required) — The booking ID to reschedule, as a plain string (e.g. '12345'). Required.
- `start` (string, required) — New start time in ISO 8601 / RFC 3339 UTC format (e.g. '2024-08-13T09:00:00Z'). Required.
- `end` (string, required) — New end time in ISO 8601 / RFC 3339 UTC format (e.g. '2024-08-13T09:30:00Z'). Required.
```

**Output `data` schema:**

```typescript
{
  before?: {
    id?: number | null;
    uid?: string | null;
    title?: string | null;
    description?: string | null;
    status?: string | null;
    start?: string | null;
    end?: string | null;
    duration?: number | null;
    eventTypeId?: number | null;
    meetingUrl?: string | null;
    location?: string | null;
    absentHost?: boolean | null;
    cancellationReason?: string | null;
    rescheduledFromUid?: string | null;
    rescheduledToUid?: string | null;
    attendees?: {
      name?: string | null;
      email?: string | null;
      timeZone?: string | null;
      phoneNumber?: string | null;
      language?: string | null;
      absent?: boolean | null;
    }[] | null;
    hosts?: object[] | null;
  } | null;
  after?: { /* same shape as `before` */ } | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>confirm_booking</code> — Confirm a pending booking</summary>

Confirm a pending booking. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the booking's current status — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `booking_id` (string, required) — ID of the pending booking to confirm, as a plain string (e.g. '12345'). Required.
```

**Output `data` schema:**

```typescript
{
  before?: {
    id?: number | null;
    uid?: string | null;
    title?: string | null;
    description?: string | null;
    status?: string | null;
    start?: string | null;
    end?: string | null;
    duration?: number | null;
    eventTypeId?: number | null;
    meetingUrl?: string | null;
    location?: string | null;
    absentHost?: boolean | null;
    cancellationReason?: string | null;
    rescheduledFromUid?: string | null;
    rescheduledToUid?: string | null;
    attendees?: {
      name?: string | null;
      email?: string | null;
      timeZone?: string | null;
      phoneNumber?: string | null;
      language?: string | null;
      absent?: boolean | null;
    }[] | null;
    hosts?: object[] | null;
  } | null;
  after?: { /* same shape as `before` */ } | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>mark_booking_absent</code> — Mark a booking as absent</summary>

Mark a booking as absent. Only the fields you provide are changed — others keep their current value. NOTE: this overwrites the booking's current attendance state — the original state is not stored after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `booking_id` (string, required) — ID of the booking to mark as absent, as a plain string (e.g. '12345'). Required.
```

**Output `data` schema:**

```typescript
{
  before?: {
    id?: number | null;
    uid?: string | null;
    title?: string | null;
    description?: string | null;
    status?: string | null;
    start?: string | null;
    end?: string | null;
    duration?: number | null;
    eventTypeId?: number | null;
    meetingUrl?: string | null;
    location?: string | null;
    absentHost?: boolean | null;
    cancellationReason?: string | null;
    rescheduledFromUid?: string | null;
    rescheduledToUid?: string | null;
    attendees?: {
      name?: string | null;
      email?: string | null;
      timeZone?: string | null;
      phoneNumber?: string | null;
      language?: string | null;
      absent?: boolean | null;
    }[] | null;
    hosts?: object[] | null;
  } | null;
  after?: { /* same shape as `before` */ } | null;
  // additional upstream fields may be present
}
```

</details>


### Schedules


<details>
<summary><code>get_schedules</code> — Get all schedules for the user</summary>

Get all schedules for the user

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  schedules: {
    id?: number | null;
    ownerId?: number | null;
    name?: string | null;
    timeZone?: string | null;
    isDefault?: boolean | null;
    availability?: {
      days?: string[] | null;
      startTime?: string | null;
      endTime?: string | null;
    }[] | null;
    overrides?: object[] | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_schedule</code> — Get a specific schedule by ID</summary>

Get a specific schedule by ID

**Inputs:**
```
- `schedule_id` (string, required) — The schedule ID identifying the schedule to retrieve. Plain string containing the Cal.com numeric schedule identifier (for example "12345"). Required — the call fails with a validation error if omitted or blank.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  ownerId?: number | null;
  name?: string | null;
  timeZone?: string | null;
  isDefault?: boolean | null;
  availability?: {
    days?: string[] | null;
    startTime?: string | null;
    endTime?: string | null;
  }[] | null;
  overrides?: object[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_default_schedule</code> — Get default schedule</summary>

Get default schedule

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  ownerId?: number | null;
  name?: string | null;
  timeZone?: string | null;
  isDefault?: boolean | null;
  availability?: {
    days?: string[] | null;
    startTime?: string | null;
    endTime?: string | null;
  }[] | null;
  overrides?: object[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>create_schedule</code> — Create a new schedule</summary>

Create a new schedule

**Inputs:**
```
- `name` (string, required) — Name of the schedule to create, as shown in Cal.com. Plain free-text string (for example "Working Hours"). Required — the call fails with a validation error if omitted or blank.
```

**Output `data` schema:**

```typescript
{
  id?: number | null;
  ownerId?: number | null;
  name?: string | null;
  timeZone?: string | null;
  isDefault?: boolean | null;
  availability?: {
    days?: string[] | null;
    startTime?: string | null;
    endTime?: string | null;
  }[] | null;
  overrides?: object[] | null;
  // additional upstream fields may be present
}
```

</details>


### Availability


<details>
<summary><code>get_availability</code> — Get available time slots</summary>

Get available time slots

**Inputs:**
```
- `date` (string, required) — Calendar day to look up available slots for, as a plain string in YYYY-MM-DD format (ISO 8601 calendar date). Required — there is no default, and the call fails with VALIDATION_ERROR if it is omitted or not in YYYY-MM-DD format.
```

**Output `data` schema:**

```typescript
{
  date?: string | null;
  timeZone?: string | null;
  count: number;
  slots: {
    start?: string | null;
    end?: string | null;
    time?: string | null;
    attendees?: number | null;
    bookingUid?: string | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_busy_times</code> — Get busy times from calendars</summary>

Get busy times from calendars

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  busy_times: {
    start?: string | null;
    end?: string | null;
    source?: string | null;
    title?: string | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


### Organizations


<details>
<summary><code>get_org_memberships</code> — Get organization memberships</summary>

Get organization memberships

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  memberships: {
    id?: number | null;
    userId?: number | null;
    teamId?: number | null;
    organizationId?: number | null;
    role?: string | null;
    accepted?: boolean | null;
    disableImpersonation?: boolean | null;
    user?: {
      id?: number | null;
      email?: string | null;
      username?: string | null;
      name?: string | null;
    } | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>get_org_routing_forms</code> — Get organization routing forms</summary>

Get organization routing forms

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  count: number;
  routing_forms: {
    id?: string | null;
    name?: string | null;
    description?: string | null;
    disabled?: boolean | null;
    position?: number | null;
    userId?: number | null;
    teamId?: number | null;
    routes?: any;
    fields?: any;
    createdAt?: string | null;
    updatedAt?: string | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "description", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Authentication</strong></summary>

This server uses static API-key authentication. Add your Cal.com API key to your MewCP account as the `api_key` credential field. The server sends it upstream to the Cal.com v2 API as:

```
Authorization: Bearer <api_key>
cal-api-version: 2024-06-11
```

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Booking ID:**

```
Plain string
Example: 12345
```

**Event type ID:**

```
Integer
Example: 123456
```

**Datetime:**

```
ISO 8601 / RFC 3339 UTC
Example: 2024-08-13T09:00:00Z
```

**Calendar date:**

```
YYYY-MM-DD (ISO 8601 calendar date)
Example: 2024-08-13
```

</details>


## Getting Your Cal.com API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to [Cal.com Settings → Developer → API Keys](https://app.cal.com/settings/developer/api-keys)
2. Open the **API Keys** section of your developer settings
3. Click **Add** (or **Create**) to generate a new API key
4. Copy the generated key — you will only see it once

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Cal.com credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Cal.com API key (static) in the `api_key` credential field
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Cal.com API Error</strong></summary>

- **Cause:** Upstream Cal.com API returned an error
- **Solution:**
  1. Check Cal.com service status at [Cal.com Status Page](https://status.cal.com)
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Cal.com API Documentation](https://cal.com/docs/api-reference/v2/introduction)** — Official API reference
- **[Cal.com API Reference](https://cal.com/docs/api-reference/v2/introduction)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
