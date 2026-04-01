import pandas as pd
from metro.models import UserProfile, MetroCard

def run():
    file_path = "dataset/namma_metro_dataset_10000.xlsx"

    users_df = pd.read_excel(file_path, sheet_name="Users")
    cards_df = pd.read_excel(file_path, sheet_name="MetroCards")

    # Clear old data (recommended when re-importing)
    MetroCard.objects.all().delete()
    UserProfile.objects.all().delete()

    # Import Users
    for _, row in users_df.iterrows():
        UserProfile.objects.create(
            user_id=int(row["user_id"]),
            full_name=str(row["full_name"]),
            phone=str(row["phone"]),
            email=str(row["email"]),
            has_card=(str(row["has_card"]).strip().upper() == "YES")
        )

    # Import Cards
    for _, row in cards_df.iterrows():
        profile = UserProfile.objects.filter(user_id=int(row["user_id"])).first()
        if profile:
            MetroCard.objects.create(
                user_profile=profile,
                card_number=str(row["card_number"]),
                balance=int(row["balance"]),
                issued_date=pd.to_datetime(row["issued_date"]).date() if pd.notna(row["issued_date"]) else None,
                status=str(row["status"]) if pd.notna(row["status"]) else "ACTIVE",
            )

    print("✅ Imported Users + MetroCards from Excel successfully.")
