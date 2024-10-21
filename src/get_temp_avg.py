def get_temp_avg(boxes):
    temperature_sum = 0.0
    temperature_count = 0
    temperature_names = ["temperatur", "temperature", "Temperatur", "Temperature"]
    
    # Iterate over each box
    for box in boxes:
        for sensor in box["sensors"]:
            # Check if the sensor title indicates it measures temperature
            if "title" not in sensor:
                continue

            if sensor["title"] in temperature_names:
                if "lastMeasurement" not in sensor:
                    continue

                sensor = sensor["lastMeasurement"]

                if "value" not in sensor:
                    continue

                temperature_sum += float(sensor["value"])
                temperature_count += 1
                
    if temperature_count == 0:
        return None
    
    return temperature_sum / temperature_count