# Testing & Validation Strategy (Phase 4)

This document outlines the comprehensive testing and validation matrix for the AI Voice Receptionist backend. It ensures the system is production-ready, resilient to failures, and accurately integrated with the RetellAI conversational flow.

## 1. Architecture Overview
The backend follows clean architecture principles, separating the HTTP transport layer (Routers) from core business logic (Services) and external integrations (Google Sheets API, SMTP). 
All endpoints are designed as webhooks consumed by RetellAI Function Nodes. They use consistent response shapes (`BaseResponse`) to guarantee seamless conversational mapping.

## 2. Testing Strategy
- **API Validation**: Verify strict schema adherence using Pydantic. Ensure invalid inputs are gracefully rejected with a 422 Unprocessable Content.
- **Integration Validation**: Test external services (Google Sheets, SMTP) in enabled, disabled, and failure modes.
- **Conversation Validation**: Validate the RetellAI conversation flow against intended user journeys.
- **Production Readiness**: Verify structured logging, Request IDs, error handling, and health diagnostics.

---

## 3. API Testing Matrix

### GET `/health`
- **Purpose**: Verify service health and integration status.
- **Expected Request**: No body.
- **Expected Response**: `200 OK` with `status`, `environment`, `version`, `timestamp`, `google_sheets_status`, `smtp_status`.
- **Success Criteria**: Returns 200 with all fields populated.
- **Failure Cases**: N/A.

### GET `/services`
- **Purpose**: Retrieve a list of available dental services.
- **Expected Request**: No body.
- **Expected Response**: `200 OK` with an array of services.
- **Success Criteria**: Returns 200 with the correct list of valid services.
- **Failure Cases**: N/A.

### GET `/availability`
- **Purpose**: Check available time slots for a specific date.
- **Expected Request**: Query parameter `date` (YYYY-MM-DD).
- **Expected Response**: `200 OK` with a list of available `HH:MM` slots.
- **Success Criteria**: Returns correct slots for the given date.
- **Failure Cases**: 
  - Past date → `422 Unprocessable Content`.
  - Sunday → `200 OK` with empty slots or an error indicating closed clinic. (Current logic returns standard slots if weekday validation is purely in booking).
  - Invalid format → `422 Unprocessable Content`.

### POST `/appointments/book`
- **Purpose**: Book a new appointment, persist to Sheets, send email.
- **Expected Request**: `caller_name`, `caller_phone`, `selected_service`, `preferred_date`, `preferred_time`, `caller_email` (optional).
- **Expected Response**: `200 OK` with `success=true`, `booking_id`, and confirmation message.
- **Success Criteria**: Booking ID is generated, Google Sheet is updated (if enabled), email is sent (if enabled), caller gets a 200 response.
- **Failure Cases**:
  - Sheets enabled but write fails → `503 Service Unavailable`.
  - Validation failures (past date, bad phone) → `422 Unprocessable Content`.

### POST `/appointments/cancel`
- **Purpose**: Cancel an existing appointment.
- **Expected Request**: `caller_name`, `caller_phone`, `cancel_reason` (optional).
- **Expected Response**: `200 OK` with `success=true` and cancellation message.
- **Success Criteria**: Caller is verified and marked cancelled.
- **Failure Cases**: Missing required fields → `422 Unprocessable Content`.

### POST `/appointments/reschedule`
- **Purpose**: Change appointment date/time.
- **Expected Request**: `caller_name`, `caller_phone`, `new_date`, `new_time`.
- **Expected Response**: `200 OK` with `success=true` and reschedule message.
- **Success Criteria**: Appointment is updated.
- **Failure Cases**: Validation failures (past date) → `422 Unprocessable Content`.

### POST `/faq`
- **Purpose**: Answer a clinic-related question.
- **Expected Request**: `question`.
- **Expected Response**: `200 OK` with the answer.
- **Success Criteria**: Returns a predefined answer matching the intent.
- **Failure Cases**: Missing question → `422 Unprocessable Content`.

### POST `/human-transfer`
- **Purpose**: Log a request for human agent transfer.
- **Expected Request**: `caller_name`, `caller_phone`, `reason`.
- **Expected Response**: `200 OK`.
- **Success Criteria**: Transfer request logged successfully.
- **Failure Cases**: Invalid reason → `422 Unprocessable Content`.

---

## 4. Validation Scenarios

Ensure the application robustly handles incorrect inputs:

- **Invalid Phone**: Less than 10 digits or invalid starting digit (for India) → `422 Unprocessable Content`.
- **Invalid Email**: Malformed email string → `422 Unprocessable Content` (if email format validation is strict).
- **Past Dates**: Booking in the past → `422 Unprocessable Content`.
- **Sunday Bookings**: Clinic closed on Sundays (enforced by date validator) → `422 Unprocessable Content`.
- **Unknown Services**: Service enum mismatch → `422 Unprocessable Content`.
- **Out-of-Hours Appointments**: Before 9 AM or after 6 PM → `422 Unprocessable Content`.
- **Missing Required Fields**: e.g., missing `caller_name` → `422 Unprocessable Content`.

---

## 5. Integration Scenarios

### Google Sheets Integration
- **Enabled**: Valid credentials provided. Row correctly appended.
- **Disabled**: Credentials omitted. Warning logged. Booking succeeds without persistence.
- **Failure**: Invalid credentials or network error. Catch `BookingPersistenceError` → returns `503 Service Unavailable`.

### SMTP Email Integration
- **Enabled**: Valid credentials. Email sent.
- **Disabled**: Credentials omitted. Warning logged. Booking succeeds.
- **Failure**: Invalid credentials or network error. Caught safely internally. Error logged. Booking succeeds.

---

## 6. RetellAI Conversation Validation

This involves testing the end-to-end user experience using RetellAI's console or phone call simulator:

- **Happy Path**: User books an appointment seamlessly without interruption.
- **FAQ Handling**: User asks "Where are you located?" before booking. AI responds, then guides back to booking.
- **Interruptions**: User interrupts the AI. AI pauses and gracefully adapts.
- **Fallback Handling (Max 3 Retries)**: User says something incomprehensible 3 times. AI triggers human transfer.
- **Human Transfer**: User requests to speak to a human. AI calls `/human-transfer` and transitions out.
- **Emergency**: User says they are in severe pain. AI escalates priority or advises immediate action.
- **Cancel**: User requests cancellation. AI extracts name/phone and triggers `/appointments/cancel`.
- **Reschedule**: User requests new date. AI triggers `/appointments/reschedule`.
- **Confirmation Edits**: User corrects a mistake (e.g., "Wait, I meant tomorrow") before finalizing.

---

## 7. Production Validation Checklist

- [ ] **Logging**: All requests generate a structured log entry detailing method, route, duration, and status.
- [ ] **Request IDs**: Every log entry and error response contains a unique `request_id`.
- [ ] **Health Endpoint**: `/health` accurately reflects the environment and external service enablement.
- [ ] **Global Exception Handler**: Unhandled runtime errors return a sanitized `500` JSON response (no stack trace leaks).
- [ ] **Response Consistency**: All endpoints return `success` and `message` variables mapped for RetellAI.
