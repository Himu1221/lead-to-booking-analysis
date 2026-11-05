"""Deterministic fictional data; no external sources or personal information."""
from pathlib import Path
from datetime import datetime,timedelta
import csv,random

ROOT=Path(__file__).resolve().parents[1]
def generate():
    rng=random.Random(1221)
    out=ROOT/'data';out.mkdir(exist_ok=True)
    leads=[];activities=[];quotes=[];bookings=[]
    for i in range(1,361):
        lead=f'L{i:04}'
        created=datetime(2026,1,1,8)+timedelta(days=rng.randrange(181),hours=rng.randrange(10),minutes=rng.randrange(60))
        source=rng.choice(['Website','Referral','Social media','Phone'])
        service=rng.choice(['Recurring clean','Deep clean','Move-out clean'])
        owner=rng.choice(['Team A','Team B','Team C'])
        leads.append([lead,created.isoformat(timespec='minutes'),source,service,owner])
        if rng.random()<.12:continue
        hours=rng.choice([.5,1,2,4,8,16,30,48])+rng.random()
        first=created+timedelta(hours=hours)
        activities.append([f'A{len(activities)+1:04}',lead,first.isoformat(timespec='minutes'),'First response'])
        for _ in range(rng.randrange(3)):
            follow=first+timedelta(days=rng.randrange(1,6),hours=rng.randrange(8))
            activities.append([f'A{len(activities)+1:04}',lead,follow.isoformat(timespec='minutes'),'Follow-up'])
        if rng.random()>=.74:continue
        quote_at=first+timedelta(hours=rng.randrange(1,37))
        amount={'Recurring clean':130,'Deep clean':250,'Move-out clean':320}[service]+rng.randrange(-20,61,10)
        quote=f'Q{len(quotes)+1:04}'
        quotes.append([quote,lead,quote_at.isoformat(timespec='minutes'),amount])
        # Source differences are explicit simulation assumptions, not discoveries about real businesses.
        chance={'Website':.52,'Referral':.7,'Social media':.38,'Phone':.58}[source]
        if rng.random()<chance:
            booked_at=quote_at+timedelta(days=rng.randrange(1,11),hours=rng.randrange(8))
            bookings.append([f'B{len(bookings)+1:04}',lead,quote,booked_at.isoformat(timespec='minutes')])
    for name,headers,rows in [
      ('leads',['lead_id','created_at','source','service','owner'],leads),
      ('activities',['activity_id','lead_id','occurred_at','activity_type'],activities),
      ('quotes',['quote_id','lead_id','quoted_at','quoted_amount'],quotes),
      ('bookings',['booking_id','lead_id','quote_id','booked_at'],bookings)]:
        with (out/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(headers);w.writerows(rows)
    print('Generated 360 fictional leads with seed 1221; snapshot: 2026-07-31T23:59:59.')
if __name__=='__main__':generate()
