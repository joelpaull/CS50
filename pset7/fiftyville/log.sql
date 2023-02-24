-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Gives crime scheme report (295 or 297)
SELECT id FROM crime_scene_reports
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND street = 'Humphrey Street';
-- Get descrition of crime reports from above, ours is 295
SELECT description FROM crime_scene_reports
WHERE id = '295'
OR id = '297';
-- Get statments from interviews
SELECT transcript FROM interviews
WHERE transcript
LIKE '%bakery%';
-- Get all licence plates from bakery car park between 10.15-10.25
SELECT license_plate from bakery_security_logs
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND hour = '10'
AND minute >= '15'
AND minute <= '25';
-- Get name of people corresponding to above icence plate numbers
SELECT name from people
WHERE license_plate IN
(SELECT license_plate from bakery_security_logs
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND hour = '10'
AND minute >= '15'
AND minute <= '25');
-- Get name of people at atm on Leggett street on 28jul21
SELECT people.name from people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = 'Leggett Street'
AND year = '2021'
AND month = '07'
AND day = '28';

-- Gives name of people in bakery car park and ATM are correct times
SELECT name from people
WHERE name IN


(SELECT people.name from people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = 'Leggett Street'
AND year = '2021'
AND month = '07'
AND day = '28')

AND
name IN

(SELECT name from people
WHERE license_plate IN
(SELECT license_plate from bakery_security_logs
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND hour = '10'
AND minute >= '15'
AND minute <= '25'));

--give name of people who made call and on above list
SELECT name from people
WHERE phone_number IN
(SELECT caller FROM phone_calls
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND duration < 60)
AND name IN

(SELECT name from people
WHERE name IN


(SELECT people.name from people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = 'Leggett Street'
AND year = '2021'
AND month = '07'
AND day = '28')

AND
name IN

(SELECT name from people
WHERE license_plate IN
(SELECT license_plate from bakery_security_logs
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND hour = '10'
AND minute >= '15'
AND minute <= '25')));
--Get call recievers
SELECT name from people
WHERE phone_number IN
(SELECT receiver FROM phone_calls
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND duration < 60)
-- What flight is earliest flight on 29Jul21? gives id = 36 leaving at 8.20am
SELECT flights.id FROM flights
JOIN airports ON flights.origin_airport_id = airports.id
WHERE year = '2021'
AND month = '07'
AND day = '29'
AND airports.full_name = 'Fiftyville Regional Airport'
ORDER BY hour, minute
-- was diana or bruce on flight? - what seat?
SELECT people.name, seat FROM passengers
JOIN people ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = '36'
AND people.name IN
(SELECT name from people
WHERE phone_number IN
(SELECT caller FROM phone_calls
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND duration < 60)
AND name IN

(SELECT name from people
WHERE name IN


(SELECT people.name from people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = 'Leggett Street'
AND year = '2021'
AND month = '07'
AND day = '28')

AND
name IN

(SELECT name from people
WHERE license_plate IN
(SELECT license_plate from bakery_security_logs
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND hour = '10'
AND minute >= '15'
AND minute <= '25'))));
-- who did bruce call that morning?
SELECT name from people
WHERE phone_number IN
(SELECT receiver FROM phone_calls
WHERE year = '2021'
AND month = '07'
AND day = '28'
AND duration < 60
AND caller =
(SELECT phone_number from people
WHERE name = 'Bruce'))
-- where are they flying to?
SELECT city from airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE flights.id = '36'
AND year = '2021'
AND month = '07'
AND day = '29';