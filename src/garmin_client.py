from datetime import date, timedelta
from garminconnect import Garmin


class GarminExtractorClient:
    def __init__(self, email: str, password: str):
        if not email or not password:
            raise ValueError("GARMIN_EMAIL és GARMIN_PASSWORD megadása kötelező")
        self.email = email
        self.password = password
        self.client = Garmin(email, password)

    def login(self):
        self.client.login()
        return True

    def collect_last_days(self, days_back: int = 30, device: str = "Garmin Venu SQ2") -> dict:
        self.login()
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back - 1)
        days = []

        for i in range(days_back):
            current = start_date + timedelta(days=i)
            current_str = current.isoformat()
            entry = {"date": current_str}

            for name, getter in [
                ("daily_summary", lambda: self.client.get_stats(current_str)),
                ("steps", lambda: self.client.get_steps_data(current_str)),
                ("heart_rate", lambda: self.client.get_heart_rates(current_str)),
                ("stress", lambda: self.client.get_stress_data(current_str)),
                ("body_battery", lambda: self.client.get_body_battery(current_str)),
                ("sleep", lambda: self.client.get_sleep_data(current_str)),
                ("activities", lambda: self.client.get_activities_by_date(current_str, current_str)),
            ]:
                try:
                    entry[name] = getter()
                except Exception as exc:
                    entry[name] = {"error": str(exc)}

            days.append(entry)

        return {
            "device": device,
            "range": {"start_date": start_date.isoformat(), "end_date": end_date.isoformat(), "days_back": days_back},
            "days": days,
        }
