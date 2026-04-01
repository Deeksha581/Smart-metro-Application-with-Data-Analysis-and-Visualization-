import pandas as pd
from django.contrib.auth.models import User


def import_users_from_excel(file_path, default_password="Metro@123"):
    """
    Import users from Excel file
    Columns required: full_name, email
    """

    df = pd.read_excel(file_path)

    created = 0
    skipped = 0

    for _, row in df.iterrows():
        email = str(row.get("email", "")).strip()
        full_name = str(row.get("full_name", "")).strip()

        if not email:
            skipped += 1
            continue

        if User.objects.filter(username=email).exists():
            skipped += 1
            continue

        User.objects.create_user(
            username=email,
            email=email,
            password=default_password,
            first_name=full_name
        )
        created += 1

    return created, skipped
