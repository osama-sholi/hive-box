from datetime import datetime, timedelta

# Calculate the date one hour ago
one_hour_ago = datetime.now() - timedelta(hours=1)

# Format it to RFC3339
rfc3339_date = one_hour_ago.isoformat() + 'Z'