# Mangatarem Cultural Map - Endpoint Tester (PowerShell)
# Tests all endpoints for each user role without performing CRUD operations

param(
    [string]$BaseUrl = "http://localhost:5002"
)

Write-Host "=== Mangatarem Cultural Map - Endpoint Tester ===" -ForegroundColor Cyan
Write-Host "Testing against: $BaseUrl" -ForegroundColor Yellow
Write-Host ""

# Test user credentials
$TestUsers = @{
    "admin" = @{
        Username = "admin"
        Password = "admin123"
        Role = "admin"
    }
    "contributor" = @{
        Username = "contributor1"  # Assumed to exist from seed data
        Password = "contributor123"
        Role = "contributor"
    }
    "business_owner" = @{
        Username = "business1"  # Assumed to exist from seed data
        Password = "business123"
        Role = "business_owner"
    }
    "user" = @{
        Username = "visitor1"  # Assumed to exist from seed data
        Password = "visitor123"
        Role = "user"
    }
}

# Function to test a single endpoint
function Test-Endpoint {
    param(
        [string]$Method,
        [string]$Path,
        [string]$Description,
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [int]$ExpectedStatus = 200,
        [string]$Role = "public"
    )

    $Url = "$BaseUrl$Path"
    $Status = "FAIL"
    $StatusColor = "Red"
    
    try {
        $Params = @{
            Uri = $Url
            Method = $Method
            Headers = $Headers
            UseBasicParsing = $true
            TimeoutSec = 10
            ErrorAction = "Stop"
        }
        
        if ($Body) {
            $Params.Body = $Body
        }
        
        $Response = Invoke-WebRequest @Params
        
        if ($Response.StatusCode -eq $ExpectedStatus) {
            $Status = "PASS"
            $StatusColor = "Green"
        } else {
            $Status = "FAIL (Expected $ExpectedStatus, Got $($Response.StatusCode))"
            $StatusColor = "Yellow"
        }
        
        $Details = "Status: $($Response.StatusCode)"
        if ($Response.Headers["Location"]) {
            $Details += " | Redirect: $($Response.Headers["Location"])"
        }
        
    } catch {
        $StatusCode = $_.Exception.Response.StatusCode.value__
        if ($StatusCode -eq $ExpectedStatus) {
            $Status = "PASS"
            $StatusColor = "Green"
            $Details = "Status: $StatusCode"
        } else {
            $Status = "FAIL (Expected $ExpectedStatus, Got $StatusCode)"
            $StatusColor = "Red"
            $Details = "Error: $($_.Exception.Message)"
        }
    }
    
    Write-Host "  $Method $Path" -NoNewline
    Write-Host " [$Status]" -ForegroundColor $StatusColor
    Write-Host "    $Description" -ForegroundColor Gray
    Write-Host "    $Details" -ForegroundColor DarkGray
}

# Function to login and get session cookies
function Get-LoginSession {
    param(
        [string]$Username,
        [string]$Password
    )
    
    $LoginUrl = "$BaseUrl/auth/login"
    
    # First get the login page to get CSRF token
    try {
        $LoginPage = Invoke-WebRequest -Uri $LoginUrl -UseBasicParsing -SessionVariable "Session"
        
        # Extract CSRF token if present
        $CsrfToken = $LoginPage.Inputs | Where-Object { $_.name -eq "csrf_token" } | Select-Object -ExpandProperty value
        
        # Submit login form
        $LoginData = @{
            username = $Username
            password = $Password
        }
        
        if ($CsrfToken) {
            $LoginData.csrf_token = $CsrfToken
        }
        
        $Response = Invoke-WebRequest -Uri $LoginUrl -Method POST -WebSession $Session -Body $LoginData -UseBasicParsing -MaximumRedirection 0
        
        return $Session
    } catch {
        # Even if we get a redirect, we have the session
        return $Session
    }
}

# Test public endpoints first
Write-Host "=== PUBLIC ENDPOINTS ===" -ForegroundColor Magenta
Write-Host ""

Test-Endpoint -Method "GET" -Path "/" -Description "Homepage" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/auth/login" -Description "Login page" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/auth/register" -Description "Registration page" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/auth/forgot-password" -Description "Forgot password page" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/auth/pending-approval" -Description "Pending approval page" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/" -Description "Barangay listing (public)" -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/" -Description "Business listing (public)" -ExpectedStatus 200

Write-Host ""
Write-Host "=== ADMIN ENDPOINTS ===" -ForegroundColor Magenta
Write-Host ""

# Login as admin
Write-Host "Logging in as admin..." -ForegroundColor Yellow
$AdminSession = Get-LoginSession -Username "admin" -Password "admin123"

Test-Endpoint -Method "GET" -Path "/admin/dashboard" -Description "Admin dashboard" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/users" -Description "User management" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/gallery" -Description "Gallery moderation" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/reviews" -Description "Review moderation" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/documents" -Description "Document management" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/establishments" -Description "Establishment management" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/admin/visits" -Description "Visit statistics" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200

Write-Host ""
Write-Host "=== CONTRIBUTOR ENDPOINTS ===" -ForegroundColor Magenta
Write-Host ""

# Login as contributor
Write-Host "Logging in as contributor..." -ForegroundColor Yellow
$ContributorSession = Get-LoginSession -Username "contributor1" -Password "contributor123"

Test-Endpoint -Method "GET" -Path "/barangay/dashboard" -Description "Contributor dashboard" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/attractions" -Description "Manage attractions" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/events" -Description "Manage events" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/gallery" -Description "Manage gallery" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/announcements" -Description "Manage announcements" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/reviews" -Description "Manage reviews" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/barangay/profile" -Description "Contributor profile" -Headers @{Cookie = $ContributorSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200

Write-Host ""
Write-Host "=== BUSINESS OWNER ENDPOINTS ===" -ForegroundColor Magenta
Write-Host ""

# Login as business owner
Write-Host "Logging in as business owner..." -ForegroundColor Yellow
$BusinessSession = Get-LoginSession -Username "business1" -Password "business123"

Test-Endpoint -Method "GET" -Path "/business/dashboard" -Description "Business owner dashboard" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/establishment" -Description "Manage establishment" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/rooms" -Description "Manage rooms" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/menu" -Description "Manage menu" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/reviews" -Description "Manage reviews" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/business/browse" -Description "Browse other businesses" -Headers @{Cookie = $BusinessSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200

Write-Host ""
Write-Host "=== USER (VISITOR) ENDPOINTS ===" -ForegroundColor Magenta
Write-Host ""

# Login as regular user
Write-Host "Logging in as visitor..." -ForegroundColor Yellow
$UserSession = Get-LoginSession -Username "visitor1" -Password "visitor123"

Test-Endpoint -Method "GET" -Path "/user/dashboard" -Description "User dashboard" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/user/profile" -Description "User profile" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/user/favorites" -Description "User favorites" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/user/visits" -Description "User visit history" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/user/my-events" -Description "User events" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200
Test-Endpoint -Method "GET" -Path "/user/contributions" -Description "User contributions" -Headers @{Cookie = $UserSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 200

Write-Host ""
Write-Host "=== AUTHENTICATION TESTS ===" -ForegroundColor Magenta
Write-Host ""

# Test logout
Test-Endpoint -Method "GET" -Path "/auth/logout" -Description "Logout" -Headers @{Cookie = $AdminSession.Cookies.GetCookieHeaderString($BaseUrl)} -ExpectedStatus 302

# Test protected endpoint without login
Test-Endpoint -Method "GET" -Path "/admin/dashboard" -Description "Protected endpoint without login" -ExpectedStatus 401

Write-Host ""
Write-Host "=== TESTING COMPLETE ===" -ForegroundColor Green
Write-Host ""

# Note about test users
Write-Host "NOTE: This script assumes test users exist in the database." -ForegroundColor Yellow
Write-Host "Run 'python seed_data.py' to create test users if needed." -ForegroundColor Yellow
