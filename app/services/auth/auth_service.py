import ast

from app.db.mysql_db import init_db
from .jwt_setup import create_access_token
from app.core.config import settings
from datetime import timedelta

db = init_db()

def login(email: str, password: str):
    # Check if user exists in the database with given credentials
    USER_EXISTS_QUERY = f"""
    SELECT 
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM user 
                WHERE user_email = '{email}' AND user_original_password = '{password}'
            ) 
            THEN 1 
            ELSE 0 
        END AS result;
    """
    is_user_exists = ast.literal_eval(db.run(USER_EXISTS_QUERY))

    if is_user_exists[0][0] != 0:
        
        # Get user ID from email
        get_user_id_query = f"""SELECT user_id FROM user WHERE user_email = '{email}'"""
        user_id = ast.literal_eval(db.run(get_user_id_query))[0][0]

        # Check if user has access to 'depot'
        depot_user_query = f"""
        SELECT 
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM depot 
                    WHERE depot_user_id = '{user_id}'
                ) THEN 1
                ELSE 0
            END AS user_exists;
        """
        is_depot_user = ast.literal_eval(db.run(depot_user_query))[0][0]

        # Generate JWT token if access granted
        if is_depot_user != 0:
            access_token = create_access_token(
                data={"user_id": user_id, "email": email},
                expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            )

            return {
                "is_authenticated": True,
                "access_token": access_token,
                "message": "You are logged in successfully"
            }

        # Access denied if no depot access
        else:
            return {
                "is_authenticated": False,
                "access_token": "",
                "message": "Access Denied!: Only authorized depot users are permitted to log in."
            }
    else:
        return {
            "is_authenticated": False,
            "access_token": "",
            "message": "Invalid credentials"
        }
