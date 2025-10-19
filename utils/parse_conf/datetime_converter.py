import datetime
import pytz

def seconds_time_format(seconds_value, timezone_str="UTC"):

    if seconds_value is None or not isinstance(seconds_value, int):
        return "N/A"
    
    try:
        # Get current UTC time
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        # Add the remaining seconds to the current time to calculate expiration date
        expiration_datetime_utc = now_utc + datetime.timedelta(seconds=seconds_value)


        # 08-19-25: adding in timezone converter using pytz package.
        if timezone_str == "UTC":
            local_dt = expiration_datetime_utc
        else:
            try:
                local_timezone = pytz.timezone(timezone_str) # Figure out timezone str.
                local_dt = expiration_datetime_utc.astimezone(local_timezone) # Changes to new timezone.
            except pytz.UnknownTimeZoneError:
                print(f"Warning: Received unknown timezone '{timezone_str}'. Displaying in UTC instead.")
                local_dt = expiration_datetime_utc

        return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except (ValueError, TypeError) as e:
        return f"Invalid time value: {e}"


# Collect the ISO Timestamp
def parse_iso_timestamp(iso_string, timezone_str="UTC"):

    if iso_string is None:
        return None
    
    try:
        dt_object_utc = datetime.datetime.fromisoformat(iso_string.replace('Z', "+00:00"))

        # 08-19-25: adding in timezone converter using pytz package.
        if timezone_str == "UTC":
            local_dt = dt_object_utc
        else:
            try:
                local_timezone = pytz.timezone(timezone_str) # Figure out timezone str.
                local_dt = dt_object_utc.astimezone(local_timezone) # Changes to new timezone.
            except pytz.UnknownTimeZoneError:
                print(f"Warning: Received unknown timezone '{timezone_str}'. Displaying in UTC instead.")
                local_dt = dt_object_utc


        return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except (ValueError, TypeError):
        return "\nInvalid Timestamp format"
    except Exception as e:
        return f"An unexpected error occurred: {e}"



# Assists with Major Order datetime.
def parse_numeric_timestamp(numeric_timestamp, timezone_str="UTC"):
    if not isinstance(numeric_timestamp, (int, float)):
        return "N/A"
    
    try:
        dt_object_utc = datetime.datetime.fromtimestamp(numeric_timestamp, datetime.timezone.utc)

        # Local time conversion
        if timezone_str == "UTC":
            local_dt = dt_object_utc
        else:
            try:
                local_timezone = pytz.timezone(timezone_str)
                local_dt = dt_object_utc.astimezone(local_timezone)
            except pytz.UnknownTimeZoneError:
                print(f"Warning: Received unknown timezone '{timezone_str}'. Displaying in UTC instead.")
                local_dt = dt_object_utc

        return local_dt.strftime("%Y-%m-%d %H:%M:$S %Z%z")
    except (ValueError, TypeError) as e:
        return f"Invalid numeric timestamp value: {e}"
    


# Expiration date w/ user-friendly time remaining display
def expiration_with_time_left(iso_string, timezone_str="UTC"):
    if not iso_string:
        return "N/A"
    
    try:
        # Timezone-aware datetime object in UTC
        expiration_dt_utc = datetime.date.fromisoformat(iso_string.replace("Z", "+00:00"))

        now_utc = datetime.datetime.now(pytz.utc)

        time_left = expiration_dt_utc - now_utc

        # Converting expiration time to user's local timezone
        try:
            local_timezone = pytz.timezone(timezone_str)
            expiration_dt_local = expiration_dt_utc.astimezone(local_timezone)
        except pytz.UnknownTimeZoneError:
            print(f"Warning: Unknown timezone '{timezone_str}'. Displaying in UTC.")
            expiration_dt_local = expiration_dt_utc

        formatted_expiration_date = expiration_dt_local.strftime("%Y-%m-%d %H:%M:%S %Z")

        if time_left.total_seconds() <= 0:
            return f"{formatted_expiration_date} (Expired)"
        
        

        


        return f"   {formatted_expiration_date} \n   (Time Remaining: {time_left})"
    
    except (ValueError, TypeError) as e:
        return f"Invalid timestamp format: {e}"
    


def get_expiration_from_seconds(seconds_value, timezone_str="UTC"):
    if not isinstance(seconds_value, int):
        return "N/A"
    
    try:
        # Get the current time and calculate the future expiration date
        now_utc = datetime.datetime.now(pytz.utc)
        expiration_dt_utc = now_utc + datetime.timedelta(seconds=seconds_value)
        time_left = expiration_dt_utc - now_utc

        # --- This logic is copied from your original expiration_with_time_left function ---
        try:
            local_timezone = pytz.timezone(timezone_str)
            expiration_dt_local = expiration_dt_utc.astimezone(local_timezone)
        except pytz.UnknownTimeZoneError:
            print(f"Warning: Unknown timezone '{timezone_str}'. Displaying in UTC.")
            expiration_dt_local = expiration_dt_utc

        formatted_expiration_date = expiration_dt_local.strftime("%Y-%m-%d %H:%M:%S %Z")


        total_seconds = int(time_left.total_seconds())
        if time_left.total_seconds() <= 0:
            return f"{formatted_expiration_date} (Expired)"
        
        # Calculate weeks, days, hours, etc. for the 'Time Remaining' string
        seconds = total_seconds % 60
        total_minutes = total_seconds // 60
        minutes = total_minutes % 60
        total_hours = total_minutes // 60
        hours = total_hours % 24
        total_days = total_hours // 24
        days = total_days % 7
        weeks = total_days // 7

        # Put together the final string
        time_parts = []
        if weeks > 0:
            time_parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days > 0:
            time_parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0:
            time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        time_left_str = ", ".join(time_parts)
        if not time_left_str:
            time_left_str = "Less than a second."

        return f"{formatted_expiration_date} (Time Remaining: {time_left_str})"
    
    except (ValueError, TypeError) as e:
        return f"Invalid timestamp format: {e}"
    

# Used in galaxy_stats_parser for total time played
def format_duration_from_seconds(total_seconds):

    if not isinstance(total_seconds, (int, float)) or total_seconds < 0:
        return "N/A at this time."
    
    if total_seconds == 0:
        return "0 seconds."
    

    seconds_in_minute = 60
    seconds_in_hour = 3600
    seconds_in_day = 86400
    seconds_in_week = 604800
    seconds_in_month = int(30.44 * seconds_in_day)
    seconds_in_year = int(365.25 * seconds_in_day)

    # Calculations for each time unit
    years = int(total_seconds // seconds_in_year)
    remainder_seconds = total_seconds % seconds_in_year

    months = int(remainder_seconds // seconds_in_month)
    remainder_seconds %= seconds_in_month

    weeks = int(remainder_seconds // seconds_in_week)
    remainder_seconds %= seconds_in_week

    days = int(remainder_seconds // seconds_in_day)
    remainder_seconds %= seconds_in_day

    hours = int(remainder_seconds // seconds_in_hour)
    remainder_seconds %= seconds_in_hour

    minutes = int(remainder_seconds // seconds_in_minute)
    seconds = int(remainder_seconds % seconds_in_minute)

    # Final time strings
    time_sections = []
    if years > 0:
        time_sections.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        time_sections.append(f"{months} month{'s' if months != 1 else ''}")
    if weeks > 0:
        time_sections.append(f"{weeks} week{'s' if weeks != 1 else ''}")
    if days > 0:
        time_sections.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        time_sections.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        time_sections.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds >= 0:
        time_sections.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(time_sections)
        