clear;
data = readtable("data.xlsx");

DCData = readtable("OnlineData\Commercial-Office.csv");
loadShedding = readtable("LoadsheddingDetailed.xlsx")%readtable("OnlineData\LoadSheddingHistory.xlsx");


Area15Idx = (loadShedding.Area == "Area 15");

loadShedding = loadShedding(Area15Idx,:);





% Join tables
data = outerjoin(data,loadShedding,"Type","left","LeftKeys",["date",...
    "time"],"RightKeys",["Date","Time"])

ActiveShedding = ~isnan(data.Time);
plot(data.date, data.ptot)
hold on
plot(data.date,ActiveShedding*50, "r")
hold off
legend("Menzies Load","Loadshedding UCT");
title("Menzies electrical load & Loadshedding at UCT")
xlabel("Date")
ylabel("Power in kW")