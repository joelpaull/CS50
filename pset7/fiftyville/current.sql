SELECT city from airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE flights.id = '36'
AND year = '2021'
AND month = '07'
AND day = '29';