import pandas as pd
import sql_connection
import os
import threading
from datetime import datetime

light_version = None


def get_app_config():
    sqlalchemy_engine = sql_connection.get_sqlalchemy_engine()
    config_frame = pd.read_sql_query(
        "SET NOCOUNT ON; EXEC dbo.Read_Config", sqlalchemy_engine
    )
    config = {}
    for i in range(len(config_frame)):
        config[config_frame["Parameter"].iloc[i]] = config_frame["Value"].iloc[i]
    sqlalchemy_engine.dispose()

    return config


def app_logging(client_info, type, message):
    host_name = os.popen("hostname").read()
    pyodbc_connection = sql_connection.get_pyodbc_connection()
    cursor = pyodbc_connection["cursor"]
    cursor.execute(
        "EXEC dbo.Logging_App @HostName=?, @ClientInfo=?, @Type=?, @Message=?",
        host_name,
        client_info,
        type,
        message,
    )
    cursor.commit()
    pyodbc_connection["connection"].close()
    print("app_logging: " + type + ": " + message)


def get_available_sessions():
    sqlalchemy_engine = sql_connection.get_sqlalchemy_engine()
    sessions_frame = pd.read_sql_query(
        "SET NOCOUNT ON; EXEC dbo.Read_AvailableSessions", sqlalchemy_engine
    )
    sqlalchemy_engine.dispose()

    return sessions_frame


def read_session_data(event_id, session_name):

    time_start = datetime.now()

    def read_sp(
        sqlalchemy_engine, sp_suffix, event_id, session_name, data_dict_list, data_key
    ):

        if data_key == "track_map":
            sql = f"EXEC dbo.Read_{sp_suffix} @EventId={event_id};"
        else:
            sql = f"EXEC dbo.Read_{sp_suffix} @EventId={event_id}, @SessionName='{session_name}';"

        data = pd.read_sql_query("SET NOCOUNT ON; " + sql, sqlalchemy_engine)
        data_dict = {data_key: data}
        data_dict_list.append(data_dict)
        print("appended " + data_key)

    sqlalchemy_engine = sql_connection.get_sqlalchemy_engine()

    sp_dict = {
        "track_map": "TrackMap",
        "lap_times": "LapTimes",
        "sector_times": "SectorTimes",
        "conditions_data": "ConditionsData",
        "session_drivers": "SessionDrivers",
        "car_data_norms": "CarDataNorms",
    }

    if light_version:
        sp_dict.pop("car_data_norms")

    data_dict_list = []
    threads = []
    for key in sp_dict:
        # Start a new thread and have it append dataset to data_dict_list
        thread = threading.Thread(
            target=read_sp,
            daemon=True,
            args=(
                sqlalchemy_engine,
                sp_dict[key],
                event_id,
                session_name,
                data_dict_list,
                key,
            ),
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    sqlalchemy_engine.dispose()

    # Turn list of single item dicts into a dict
    data_dict = {}
    for dict in data_dict_list:
        data_key = list(dict.keys())[0]
        data_dict[data_key] = dict[data_key]

    print("Time taken: " + str(datetime.now() - time_start))

    return data_dict


def read_car_data(event_id, session_name, lap_ids):

    sqlalchemy_engine = sql_connection.get_sqlalchemy_engine()

    sql = f"EXEC dbo.Read_CarData @EventId={event_id}, @SessionName='{session_name}', @LapIdA={lap_ids[0]}"

    if len(lap_ids) == 2:
        sql += f", @LapIdB={lap_ids[1]};"
    else:
        sql += ", @LapIdB=NULL;"

    data = pd.read_sql_query("SET NOCOUNT ON; " + sql, sqlalchemy_engine)

    sqlalchemy_engine.dispose()

    return data
