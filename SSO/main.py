import json
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_sso.sso.google import GoogleSSO

app = FastAPI()

# Replace with your actual Google API credentials
CLIENT_ID = "808583469127-vdok1207i7asec52bakknkla2f9rvlr2.apps.googleusercontent.com"
CLIENT_SECRET = "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"
OAUTH_URL = "http://localhost:5000"  # Update with your actual server URL

google_sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=OAUTH_URL + "/callback",
    allow_insecure_http=True,
)

# OAuth2 Authorization Code Bearer for Authorization Header
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl=OAUTH_URL + "/auth/login",
)

# Store user data in session for demonstration purposes
user_sessions = {}

def get_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id not in user_sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_sessions[session_id]

@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Login</title>
    </head>
    <body>
        <h1>Sign in with your Google Account</h1>
        <a href="/auth/login">Login with Google</a>
    </body>
    </html>
    """

@app.get("/auth/login")
async def auth_init():
    return await google_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})

@app.get("/callback", response_class=HTMLResponse)
async def auth_callback(request: Request, user: GoogleSSO = Depends(google_sso.verify_and_process)):
    if not user:
        raise HTTPException(status_code=500, detail="Failed to retrieve user information")

    # Convert the OpenID object to a JSON-serializable format
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "display_name": user.display_name,
        "provider": user.provider,
        "picture": user.picture,
    }

    # Store user data in session (for demonstration purposes)
    session_id = "session_" + user_data["id"]
    user_sessions[session_id] = user_data

    # Set session_id cookie in the response
    response = RedirectResponse(url="/dashboard")
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(user: dict = Depends(get_user)):
    # Render dashboard with user profile picture
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>User Dashboard</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                }}
                header {{
                    background-color: #f1f1f1;
                    padding: 10px;
                    text-align: right;
                }}
                main {{
                    padding: 20px;
                }}
                img.profile-picture {{
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                }}
            </style>
        </head>
        <body>
            <header>
                <a href="/user/profile">
                    <img src="{user['picture']}" alt="Profile Picture" class="profile-picture">
                </a>
            </header>
            <main>
                <h1>Welcome to Your Dashboard, {user['display_name']}!</h1>
                <!-- Other dashboard content goes here -->
            </main>
        </body>
        </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/user/profile", response_class=HTMLResponse)
async def user_profile(user: dict = Depends(get_user)):
    # Render user profile page
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Profile</title>
        </head>
        <body>
            <h1>User Profile</h1>
            <img src="{user['picture']}" alt="Profile Picture" style="width: 100px; height: 100px; border-radius: 50%;">
            <p>ID: {user['id']}</p>
            <p>Email: {user['email']}</p>
            <p>Name: {user['display_name']}</p>
        </body>
        </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
