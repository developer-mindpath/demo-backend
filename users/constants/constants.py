# HTTP status codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401

# Messages
SIGNUP_SUCCESS = {"status": "success", "message": "User created successfully", "user_id": ""}
SIGNUP_ERROR = {"status": "error", "message": "Signup failed"}

LOGIN_SUCCESS = {"status": "success", "message": "Login successful", "user_id": ""}
LOGIN_INVALID_CREDENTIALS = {"status": "error", "message": "Invalid email or password"}
LOGIN_ERROR = {"status": "error", "message": "Invalid request"}

LOGOUT_SUCCESS = {"status": "success", "message": "Logout successful"}
LOGOUT_ERROR = {"status": "error", "message": "Invalid token"}

PROFILE_SUCCESS = {"status": "success", "message": "Profile retrieved successfully"}
PROFILE_ERROR = {"status": "error", "message": "Invalid token"}

PROJECT_TITLE = "Django Project"

USER_ID = "user_id"
