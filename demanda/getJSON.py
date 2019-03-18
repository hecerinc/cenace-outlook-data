from datetime import datetime
from datetime import timedelta



startDate = datetime(2019,1,1)
endDate = datetime(2019,2,27)

url = "https://ws01.cenace.gob.mx:8082/SWCAEZC/SIM/BCS/MDA/{}/{}/JSON"

x = startDate
while x <= endDate:
	datestr = x.strftime("%Y/%m/%d")
	delta = x + timedelta(days = 6)
	deltastr = delta.strftime("%Y/%m/%d")
	print(url.format(datestr, deltastr))
	x = delta + timedelta(days=1)

