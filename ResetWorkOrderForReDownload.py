import sys
import configparser
import pyodbc
import time
from prettytable import from_db_cursor


def main():
    try:
        tool_configuration = configparser.ConfigParser()

        #ini_path = sys.path[0] + '\configurationFile.ini'
        ini_path = sys.executable.replace("ResetWorkOrderForReDownload.exe", "configurationFile.ini")
        #print(f"Warning: ini config = {ini_path}")
        #time.sleep(10)
        tool_configuration.read(ini_path)

        default_settings = tool_configuration["DEFAULT"]

        server_name = default_settings["server_name"]
        database_name1 = default_settings["database_name1"]
        database_name2 = default_settings["database_name2"]
        database_user_id = default_settings["user_id"]
        database_password = default_settings["database_password"]

        input_work_order_id = input("Info: Please enter single/multiple work order id delimited in coma(e.g. 123,345):")

        if len(input_work_order_id) > 0:
            input_facility_code = input("Info: Please enter facility code(1 -> Mandaue or 2 -> Legaspi)")

            if len(input_facility_code) == 0:
                print("Error: Empty facility code found!")
            else:
                sql_statement = "SELECT FileName, DateDetected, DownloadStatus, RetryCounter " \
                                "FROM [CHVDP_FTP_Files] " \
                                "where replace(replace(FileName,'.xml',''),'.pdf','') " \
                                "in('" + input_work_order_id.replace(",","','") + "') " \
                                "order by DateDetected desc"
                #breakpoint()
                use_database = database_name1 if input_facility_code == '1' else database_name2
                #breakpoint()
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=' + server_name + ';'
                                      'Database=' + use_database + ';'
                                      'UID=' + database_user_id + ';'
                                      'PWD=' + database_password + ';'
                                      'Trusted_Connection=No')
                #breakpoint()

                cursor = conn.cursor()
                cursor.execute(sql_statement)

                print(from_db_cursor(cursor))

                continue_with_reset_flag = input("Info: Continue with reset(y/n)?")

                if continue_with_reset_flag == "y":
                    sql_statement = "UPDATE [CHVDP_FTP_Files] " \
                                    "SET [DownloadStatus] = 'NEW' " \
                                    ",[DateDownloaded] = NULL " \
                                    ",[ErrorMessage] = NULL " \
                                    ",[DownloaderId] = NULL " \
                                    ",[DateAllocated] = NULL " \
                                    ",[RetryCounter] = NULL " \
                                    "where replace(replace(FileName,'.xml',''),'.pdf','') in('" + input_work_order_id.replace(",","','") + "')"
                    #breakpoint()
                    cursor.execute(sql_statement)
                    cursor.commit()

                    print(f"Info: Done with reset on order id's " + input_work_order_id + ".")
                else:
                    print("Warning: Exiting application.")
                    time.sleep(5)

                #for row in cursor:
                #    print(row)
        else:
            print("Error: Empty work order placed!")
            time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        input()


main()
