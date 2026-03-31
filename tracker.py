import tkinter as tk
from tkinter import messagebox
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from tkintermapview import TkinterMapView

# Dictionary of Karachi areas with coordinates
karachi_areas = {
    "Saddar": {"lat": 24.853, "lon": 67.021},
    "Gulshan-e-Iqbal": {"lat": 24.920, "lon": 67.112},
    "Clifton": {"lat": 24.813, "lon": 67.030},
    "Korangi": {"lat": 24.830, "lon": 67.150},
    "Malir": {"lat": 24.893, "lon": 67.198}
}

def get_location_for_number(phone_number, selected_area):
    try:
        parsed_number = phonenumbers.parse(phone_number, "PK")
        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)

        if "Pakistan" in country:
            coords = karachi_areas[selected_area]
            return {
                "country": country,
                "carrier": carrier_name,
                "time_zones": time_zones,
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "full_address": selected_area + ", Karachi"
            }
        else:
            return None
    except Exception as e:
        print(f"Error parsing number: {e}")
        return None

def track_number():
    phone_number = entry.get()
    selected_area = area_var.get()  # Get selected Karachi area from dropdown
    location_data = get_location_for_number(phone_number, selected_area)

    if location_data:
        latitude = location_data['latitude']
        longitude = location_data['longitude']
        full_address = location_data['full_address']

        result_text.set(
            f"Country: {location_data['country']}\n"
            f"Carrier: {location_data['carrier']}\n"
            f"Time Zones: {', '.join(location_data['time_zones'])}\n"
            f"Location: {full_address}\n"
            f"Latitude: {latitude}, Longitude: {longitude}"
        )

        # Show map and marker
        map_widget.set_position(latitude, longitude)
        map_widget.set_zoom(12)
        map_widget.set_marker(latitude, longitude, text=full_address)
    else:
        messagebox.showerror("Error", "Number not detected in Pakistan or invalid.")

# GUI setup
root = tk.Tk()
root.title("Phone Number Tracker")
root.geometry("850x500")
root.configure(bg="#f2f4f8")

frame = tk.Frame(root, bg="#f2f4f8")
frame.pack(padx=20, pady=20)

form_frame = tk.Frame(frame, bg="#f2f4f8")
form_frame.pack(side=tk.LEFT, padx=20)

map_frame = tk.Frame(frame, bg="#f2f4f8")
map_frame.pack(side=tk.LEFT, padx=20)

tk.Label(form_frame, text="Enter Phone Number:", font=("Arial", 14), bg="#f2f4f8").pack(pady=10)
entry = tk.Entry(form_frame, font=("Arial", 14), width=20)
entry.pack(pady=5)

# Dropdown for Karachi area selection
tk.Label(form_frame, text="Select Karachi Area:", font=("Arial", 14), bg="#f2f4f8").pack(pady=10)
area_var = tk.StringVar(value="Saddar")
area_dropdown = tk.OptionMenu(form_frame, area_var, *karachi_areas.keys())
area_dropdown.config(font=("Arial", 12))
area_dropdown.pack(pady=5)

tk.Button(form_frame, text="Track", font=("Arial", 12), command=track_number,
          bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=10)

result_text = tk.StringVar()
tk.Label(form_frame, textvariable=result_text, font=("Arial", 12), bg="#f2f4f8").pack(pady=10)

map_widget = TkinterMapView(map_frame, width=400, height=300)
map_widget.pack(pady=10)

root.mainloop()

