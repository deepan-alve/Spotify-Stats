"""
Spotify Refresh Token Generator
Run this script to get your SPOTIFY_REFRESH_TOKEN
"""
import requests
from base64 import b64encode
from urllib.parse import urlencode
import webbrowser

# Fill these in from your Spotify Developer Dashboard
SPOTIFY_CLIENT_ID = input("Enter your SPOTIFY_CLIENT_ID: ").strip()
SPOTIFY_CLIENT_SECRET = input("Enter your SPOTIFY_SECRET_ID: ").strip()
REDIRECT_URI = input("Enter your callback URL (e.g., https://spotify-stats-q7nq.vercel.app/callback): ").strip()

# Scopes needed for the app
SCOPES = "user-read-currently-playing user-read-recently-played user-top-read"

def get_auth_url():
    """Generate the Spotify authorization URL"""
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return auth_url

def get_refresh_token(auth_code):
    """Exchange authorization code for refresh token"""
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

print("\n" + "="*70)
print("SPOTIFY REFRESH TOKEN GENERATOR")
print("="*70)

# Step 1: Open authorization URL
auth_url = get_auth_url()
print("\n1. Opening Spotify authorization page in your browser...")
print(f"\n   If it doesn't open automatically, visit:\n   {auth_url}\n")
webbrowser.open(auth_url)

# Step 2: Get the authorization code from callback
print("2. After authorizing, you'll be redirected to your callback URL.")
print("   The URL will look like:")
print(f"   {REDIRECT_URI}?code=AQD...xyz")
print("\n3. Copy the ENTIRE URL from your browser address bar and paste it below:\n")

callback_url = input("Paste the full callback URL here: ").strip()

# Extract the code parameter
try:
    if "code=" in callback_url:
        auth_code = callback_url.split("code=")[1].split("&")[0]
        print(f"\n✓ Authorization code extracted: {auth_code[:20]}...")
        
        # Step 3: Exchange for tokens
        print("\n4. Exchanging authorization code for tokens...")
        tokens = get_refresh_token(auth_code)
        
        if tokens:
            print("\n" + "="*70)
            print("SUCCESS! Here are your tokens:")
            print("="*70)
            print(f"\nAccess Token (expires in 1 hour):\n{tokens.get('access_token')}")
            print(f"\n\nRefresh Token (use this in your .env file):\n{tokens.get('refresh_token')}")
            print(f"\n\nToken Type: {tokens.get('token_type')}")
            print(f"Expires In: {tokens.get('expires_in')} seconds")
            print(f"Scope: {tokens.get('scope')}")
            
            print("\n" + "="*70)
            print("ADD THIS TO YOUR VERCEL ENVIRONMENT VARIABLES:")
            print("="*70)
            print(f"\nSPOTIFY_CLIENT_ID={SPOTIFY_CLIENT_ID}")
            print(f"SPOTIFY_SECRET_ID={SPOTIFY_CLIENT_SECRET}")
            print(f"SPOTIFY_REFRESH_TOKEN={tokens.get('refresh_token')}")
            print("\n" + "="*70)
            
            # Save to .env file
            save = input("\nDo you want to save these to .env file? (y/n): ").strip().lower()
            if save == 'y':
                with open('.env', 'w') as f:
                    f.write(f"SPOTIFY_CLIENT_ID={SPOTIFY_CLIENT_ID}\n")
                    f.write(f"SPOTIFY_SECRET_ID={SPOTIFY_CLIENT_SECRET}\n")
                    f.write(f"SPOTIFY_REFRESH_TOKEN={tokens.get('refresh_token')}\n")
                print("\n✓ Saved to .env file!")
        else:
            print("\n✗ Failed to get tokens. Check your credentials and try again.")
    else:
        print("\n✗ Error: No 'code' parameter found in the URL.")
        print("Make sure you copied the COMPLETE URL after authorization.")
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("Please make sure you copied the complete callback URL.")
