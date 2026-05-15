## ADDED Requirements

### Requirement: Login Page Display
The system SHALL display a login page with TomiLomos branding and an email/password form.

#### Scenario: Login page loads
- **WHEN** the user navigates to `/login`
- **THEN** the system displays a centered card with the TomiLomos logo (ChefHat icon + "TomiLomos" text), email input, password input, and a "Sign In" button
- **AND** the page has a Framer Motion entrance animation

#### Scenario: Already authenticated
- **WHEN** the user navigates to `/login` while already having a valid token in the auth store
- **THEN** the system redirects to `/app/dashboard`

### Requirement: Login Form Validation
The system SHALL validate email and password fields before submission.

#### Scenario: Valid form submission
- **WHEN** the user enters a valid email and a non-empty password and clicks "Sign In"
- **THEN** the form submits and calls the login API

#### Scenario: Empty email
- **WHEN** the user submits with an empty email field
- **THEN** the system displays an inline error "Email is required" below the email input

#### Scenario: Invalid email format
- **WHEN** the user enters an invalid email (e.g., "notanemail") and submits
- **THEN** the system displays an inline error "Invalid email format" below the email input

#### Scenario: Empty password
- **WHEN** the user submits with an empty password field
- **THEN** the system displays an inline error "Password is required" below the password input

### Requirement: Successful Login
The system SHALL authenticate the user via the backend and store the session.

#### Scenario: Login succeeds
- **WHEN** the user submits valid credentials and the backend returns a 200 with a token
- **THEN** the system decodes the JWT payload to extract user_id (sub) and tenant_id
- **AND** the system stores the token, tenant_id, and user_id in the auth store
- **AND** the system navigates to `/app/dashboard`
- **AND** the "Sign In" button shows a loading spinner during the API call

### Requirement: Login Error Handling
The system SHALL display appropriate error messages for login failures.

#### Scenario: Invalid credentials
- **WHEN** the backend returns a 401 error (wrong email or password)
- **THEN** the system displays "Invalid email or password" in an error message below the form
- **AND** the password field is cleared
- **AND** the form remains otherwise filled so the user can retry

#### Scenario: Server error
- **WHEN** the backend returns a 500 error
- **THEN** the system displays "Server error. Please try again later." below the form

#### Scenario: Network error
- **WHEN** the API call fails due to a network error (no response)
- **THEN** the system displays "Connection failed. Check your network and try again." below the form
- **AND** a "Retry" button appears next to the error message

### Requirement: Login Page Visual Design
The system SHALL present the login page with a polished, professional appearance.

#### Scenario: Visual layout
- **WHEN** viewing the login page
- **THEN** the page SHALL be full-screen with a subtle gradient background (gray-50 to white)
- **AND** the login card SHALL be centered, with white background, rounded corners, and a shadow
- **AND** the card SHALL contain the TomiLomos branding, form fields, and button
- **AND** error messages SHALL animate in (Framer Motion fade + slide)
