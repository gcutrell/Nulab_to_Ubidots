import sys
import pandas
import numpy
from datetime import datetime

def write_results(in_file, result, error_msg = "Error"):
    #Append the correct data flag (result) to the data file
    with open(in_file, "a") as raw_data:
        raw_data.write(",%d\n\r" % result)

    with open("check_data_results.txt", 'w') as result_file:
        if result == 0:
            result_file.write("%d" % result)
        else:
            result_file.write(error_msg)
        

def check_slope(in_file, column):
    #extract column and timestamps from data:
    data = pandas.read_csv(in_file,
            usecols = ['#MM/DD/YY HH:mm:SS', column]).dropna()
    print str(data.tail(10))

    #translate date strings to timestamps
    data['#MM/DD/YY HH:mm:SS'] = data['#MM/DD/YY HH:mm:SS'].apply(
            lambda x: float(datetime.strptime(x, '%m/%d/%Y %H:%M:%S').strftime("%s.%f")))

    #Calculate slope of LS regression for the last 10 data points
    data_10 = data.tail(10)
    slope_10 = numpy.polyfit(data_10.iloc[:,0], data_10.iloc[:,1], 1)[0]

    data_3 = data.tail(3)
    slope_3 = numpy.polyfit(data_3.iloc[:,0], data_3.iloc[:,1], 1)[0]

    if abs(slope_3) > 1.3 * abs(slope_10) and len(data[column]> 10):
        write_results(in_file, 1,
                        "Potential bad data in %s, %s column. The slope of the last 10 data points is %e, the slope of the last 3 data points is %e.\r\n" 
            % (in_file, column, slope_10, slope_3))
    else:
        write_results(in_file, 0)

if __name__ == '__main__':
    check_slope(sys.argv[1], sys.argv[2])
