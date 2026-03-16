# User Login Flowchart

This document provides a visual representation of the authentication flows in the Interactive Digital Cultural Map system, based on the implementation in `routes/auth.py`.

## 1. Standard Login Flow

```mermaid
graph TD
    Start([Start]) --> LoginGet[GET /login]
    LoginGet --> LoginView[Show Login Form]
    LoginView --> FormSubmit[Submit Username/Password]
    FormSubmit --> AuthCheck{Authenticate Credentials}
    
    AuthCheck -- Invalid --> FlashError[Flash: Invalid Credentials]
    FlashError --> LoginGet
    
    AuthCheck -- Valid --> RoleCheck{Check User Role}
    
    RoleCheck -- Contributor --> ApprovalCheck{Is Approved?}
    ApprovalCheck -- No --> PendingPage[Redirect /pending-approval]
    ApprovalCheck -- Yes --> BarangayDashboard[Redirect /barangay_dashboard]
    
    RoleCheck -- Admin --> AdminDashboard[Redirect /admin_dashboard]
    RoleCheck -- User --> UserDashboard[Redirect /user/dashboard]
    RoleCheck -- Other --> DefaultIndex[Redirect /index]
```

## 2. Google OAuth Login Flow

```mermaid
graph TD
    GoogleStart([Google Sign-In Clicked]) --> TokenRecv[Receive Google JWT]
    TokenRecv --> VerifyJWT{Verify Token}
    
    VerifyJWT -- Invalid --> GoogleFail[Flash: Invalid Token]
    GoogleFail --> LoginGet[Redirect /login]
    
    VerifyJWT -- Valid --> EmailCheck{Email Registered?}
    
    EmailCheck -- Yes --> RestrictionCheck{Is Admin or Contributor?}
    RestrictionCheck -- Yes --> RoleRestricted[Flash: Restricted from Google Login]
    RoleRestricted --> LoginGet
    
    RestrictionCheck -- No --> UserLogin[Log in as Registered User]
    UserLogin --> UserDash[Redirect /user/dashboard]
    
    EmailCheck -- No --> CreateAccount[Create New User Account]
    CreateAccount --> NewUserLogin[Log in as New User]
    NewUserLogin --> NewUserDash[Redirect /user/dashboard]
```

## 3. Password Reset Flow

```mermaid
graph TD
    ForgotStart([Forgot Password Clicked]) --> ForgotGet[GET /forgot-password]
    ForgotGet --> EmailForm[Show Email Form]
    EmailForm --> EmailSubmit[Submit Email Address]
    EmailSubmit --> UserSearch{User Exists?}
    
    UserSearch -- Yes --> GenToken[Generate Reset Token]
    GenToken --> SendEmail[Send Reset Email]
    SendEmail --> SuccessMsg[Flash: Success Check Inbox]
    
    UserSearch -- No --> SuccessMsg
    
    SuccessMsg --> ForgotGet
    
    TokenEmail([User Clicks Email Link]) --> ResetGet[GET /reset-password/token]
    ResetGet --> TokenValid{Is Token Valid?}
    
    TokenValid -- No --> ResetExp[Flash: Token Expired/Invalid]
    ResetExp --> ForgotGet
    
    TokenValid -- Yes --> ResetForm[Show New Password Form]
    ResetForm --> FormSubmitPass[Submit New Password]
    FormSubmitPass --> PassValidate{Passwords Match & Length?}
    
    PassValidate -- No --> PassError[Flash: Validation Error]
    PassError --> ResetForm
    
    PassValidate -- Yes --> UpdatePass[Update Password & Mark Token Used]
    UpdatePass --> LoginRedirect[Flash: Success Redirect /login]
```

## 4. Logout Flow

```mermaid
graph TD
    LogoutStart([Click Logout]) --> LogoutReq[GET /logout]
    LogoutReq --> EndSession[Terminate User Session]
    EndSession --> HomeRedirect[Redirect /index]
```
