establishment
Azamgarh        6
Bilari         18
Dhanaura        6
Dholana        18
Jagdishpur     18
Rudauli        18
Sikandrabad     6


total ac = 403 as needed *9 rows = 3618  [EXACT_match]

5  -         DATA IS NOT PRESENT


CURRENT ROWS = 3618-5 = [3613]

from collections import Counter
counts = Counter([i.split('-')[0] for i in data])
divisor = 9
for item, count in counts.items():
    if count % divisor != 0:
        print(f"'{item}' appears {count} times and is divisible by {divisor}")
    
""""""""""""""""""""""

# PDF ARE NOT AVAILABLE

'Amethi' appears 8 times and is divisible by 9    addition , april
'Chandausi' appears 8 times and is divisible by 9  sambhal chandausi, may ,modification
'Kairana' appears 8 times and is divisible by 9   shamli/ kahirana /may /deletion
'Khadda' appears 8 times and is divisible by 9   khushinagar/khadda/may/deletion
'Khaga' appears 8 times and is divisible by 9     fatehpur\Khaga\modification\MARCH-2025
'Lucknow North' appears 8 times and is divisible by 9    -  \Lucknow\Lucknow North\modification\MARCH-2025 not available

