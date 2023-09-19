classdef loadMenziesData
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here

    properties
        data
    end

    methods
        function obj = loadMenziesData()
            %UNTITLED Construct an instance of this class
            %   Detailed explanation goes here

            data = readtable("data.xlsx");

            %Remove data with no information
            data = removevars(data, ["meter_serial", "tstamp","meter_desc", "expwh","difference_exp_kwh","interval_start", "waste", "meter_id", "tariff_id","tou", "impwh","stot", "pftot","md","qtot","difference_imp_kwh"]);

            %data.impwh = erase(data.impwh,',');
            data.epoch_timestamp = erase(data.epoch_timestamp, ',');
            data.epoch_timestamp = str2double(data.epoch_timestamp);


            data.day = day(data.date, "iso-dayofweek");
            data.date = day(data.date, "dayofyear");
            data.month = month(data.date);

            low_time = 0.29;
            up_time = 0.75;

            wrkHrsCondition = (data.time >= low_time) & (data.time <= up_time) & (data.day ~= 6) & (data.day ~= 7);
            dayTimeCondition =  (data.time >= low_time) & (data.time <= up_time);
            weekDayCondition = (data.day ~= 6) & (data.day ~= 7) ;

            data.wrkHr      = wrkHrsCondition;

            data.dayTime    =  dayTimeCondition;

            data.weekDay    = weekDayCondition;

            data = rmmissing(data);
            % Fill outliers
            dataTest1 = filloutliers(data,"linear","percentiles",[4.75 100],"DataVariables","ptot");          
            obj.data = dataTest1;
        end

        function outputArg = method1(obj)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.data ;
        end
    end
end