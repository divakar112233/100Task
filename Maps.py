import os
import json
import time
import pandas as pd
from google.maps import places_v1
from google.type import latlng_pb2

def google_maps_scraper():
    print("🌍 Google Maps Data Scraper (Official API)\n")
    
    api_key = input("Enter your Google Places API Key: ").strip()
    if not api_key:
        print("❌ API Key required!")
        return

    # Search parameters
    query = input("Search query (e.g., restaurants, hospitals): ").strip()
    lat = float(input("Latitude (e.g., 13.0827 for Chennai): ") or 13.0827)
    lng = float(input("Longitude (e.g., 80.2707 for Chennai): ") or 80.2707)
    radius = int(input("Radius in meters (max 50000): ") or 5000)
    max_results = int(input("Max results (max 20 per request): ") or 20)

    client = places_v1.PlacesClient(client_options={"api_key": api_key})

    # Create location
    center = latlng_pb2.LatLng(latitude=lat, longitude=lng)
    circle = places_v1.Circle(center=center, radius=radius)
    location_restriction = places_v1.SearchNearbyRequest.LocationRestriction(circle=circle)

    request = places_v1.SearchNearbyRequest(
        location_restriction=location_restriction,
        max_result_count=max_results,
        # included_types=["restaurant", "cafe"]  # Add types if needed
    )

    print(f"\n🔍 Searching near ({lat}, {lng})...")
    
    try:
        response = client.search_nearby(request=request)
        
        results = []
        for place in response.places:
            data = {
                "Name": place.display_name.text if place.display_name else "N/A",
                "Address": place.formatted_address,
                "Rating": place.rating,
                "User Ratings": place.user_rating_count,
                "Types": ", ".join(place.types),
                "Place ID": place.id,
                "Latitude": place.location.latitude,
                "Longitude": place.location.longitude,
                "Website": place.website_uri,
                "Phone": place.international_phone_number,
            }
            results.append(data)
            print(f"✅ Found: {data['Name']} ({data['Rating']} ⭐)")

        # Save results
        df = pd.DataFrame(results)
        filename = f"google_maps_{query.replace(' ', '_')}_{time.strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"\n🎉 Done! {len(results)} places saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    google_maps_scraper()