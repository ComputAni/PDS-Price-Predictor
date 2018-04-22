from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import time


# Make sure to run 'pip install uber-rides' first.


# Gets the current price given the start and end locations.
def getPriceNow(startLat, startLong, endLat, endLong):
	# Left out the server token as the repo is public.
	session = Session(server_token="......................")
	client = UberRidesClient(session)

	response = client.get_price_estimates(
	    start_latitude=startLat,
	    start_longitude=startLong,
	    end_latitude=endLat,
	    end_longitude=endLong,
	    seat_count=1
	)

	estimate = response.json.get('prices')

	return estimate


# Example test for 2 minutes
# Union Square, San Francisco coordinates
startCoord = (37.787994,-122.407437)
# Santana Row, San Jose coordinates
endCoord = (37.319901,-121.948339)

# Estimate: List of dictionaries. You can pick which service you want. UberX is probably the best option - Index number 7.
# 'high_estimate', 'low_estimate' are in $, 'duration' is in seconds.
estimate = getPriceNow(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
print(estimate)

for i in range(2):
	# Sleep for a minute - it takes the parameter in seconds
	time.sleep(60)

	# Estimate: List of dictionaries. You can pick which service you want. UberX is probably the best option - Index number 7.
	# 'high_estimate', 'low_estimate' are in $, 'duration' is in seconds.
	estimate = getPriceNow(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
	print(estimate)



