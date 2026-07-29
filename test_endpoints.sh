#!/bin/bash
BASE_URL="http://localhost:5002"

# Role credentials
declare -A users=(
    ["admin"]="admin:admin123"
    ["contributor"]="steward:steward123"
    ["business_owner"]="test_owner:owner123"
    ["user"]="tourist:tourist123"
)

# Endpoints by role
declare -A endpoints=(
    ["admin"]="/admin/dashboard /admin/visits /admin/visits/registry /admin/reviews /admin/documents /admin/establishments"
    ["contributor"]="/barangay/dashboard /barangay/attractions /barangay/events /barangay/gallery /barangay/announcements /barangay/reviews /barangay/profile"
    ["business_owner"]="/business/dashboard /business/establishment/create /business/rooms /business/menu /business/reviews /business/browse"
    ["user"]="/user/dashboard /user/profile /user/favorites /user/visits /user/my-events /user/contributions"
)

for role in admin contributor business_owner user; do
    IFS=':' read -r user pass <<< "${users[$role]}"
    cookie_file="cookies_${role}.txt"
    echo "--- Testing $role ($user) ---"
    
    # 1. Get login page and CSRF token
    csrf_token=$(curl -s -c "$cookie_file" "$BASE_URL/auth/login" | grep 'name="csrf_token" value="' | sed 's/.*value="\([^"]*\)".*/\1/')
    sleep 2
    
    # 2. Login
    login_response=$(curl -s -c "$cookie_file" -b "$cookie_file" -d "username=$user&password=$pass&csrf_token=$csrf_token" -X POST -w "%{http_code}" -o /dev/null "$BASE_URL/auth/login")
    echo "Login: $login_response"

    # 3. Test endpoints
    for ep in ${endpoints[$role]}; do
        sleep 3
        response=$(curl -s -b "$cookie_file" -L -w "%{http_code}" -o /dev/null "$BASE_URL$ep")
        echo "GET $ep: $response"
    done
    
    # 4. Logout
    sleep 3
    logout_response=$(curl -s -b "$cookie_file" -L -w "%{http_code}" -o /dev/null "$BASE_URL/auth/logout")
    echo "Logout: $logout_response"
    
    rm -f "$cookie_file"
done
