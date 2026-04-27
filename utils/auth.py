"""Role-based authentication for ResQSync AI."""
import streamlit as st

DEMO_USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "Command Admin"},
    "staff": {"password": "staff123", "role": "staff", "name": "Response Staff"},
    "guest": {"password": "guest123", "role": "guest", "name": "Hotel Guest"},
}


def login(username: str, password: str) -> bool:
    """Authenticate user and set session state."""
    user = DEMO_USERS.get(username)
    if user and user["password"] == password:
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.session_state["role"] = user["role"]
        st.session_state["display_name"] = user["name"]
        return True
    return False


def logout():
    """Clear session state."""
    for key in ["authenticated", "username", "role", "display_name"]:
        st.session_state.pop(key, None)


def require_auth(allowed_roles=None):
    """Check if user is authenticated and has required role."""
    if not st.session_state.get("authenticated"):
        return False
    if allowed_roles and st.session_state.get("role") not in allowed_roles:
        return False
    return True


def get_role():
    """Get current user role."""
    return st.session_state.get("role", "guest")
