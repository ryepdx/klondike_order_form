from math import ceil

exchange_rate = 104
fee = 0.05

# Batches of 128.

K1 =  ((11.28 / exchange_rate) + # Assembly
       (7.2 / exchange_rate) + # Parts
       (6 / exchange_rate) + # Heatsink
       (13.2 / exchange_rate))  # Fabrication (rough estimate, just using K16 price for now)

K1 += K1 * fee
K1 = ceil(K1 * 100) / 100.0 # Round up to two decimal places.

K16 = ((54.75 / exchange_rate) + # Assembly
       (27.6 / exchange_rate) + # Parts
       (6 / exchange_rate) + # Heatsink
       (13.2 / exchange_rate))  # Fabrication
       
K16 += K16 * fee
K16 = ceil(K16 * 100) / 100.0 # Round up to two decimal places.

K64 = (K16 * 4) # Rule of thumb for now.
K64 = ceil(K64 * 100) / 100.0 # Round up to two decimal places.
