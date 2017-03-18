SCHEMAS = { 
    "file":
'''
CREATE TABLE file(
    file_id integer primary key AUTOINCREMENT,
    file_name text(20),         --file name for debugging and other purposes
    file_hash text(64),         --hash to identify inported files
    creation_date datetime,     --file creation time
    event_name text(30),        --e.g. Swimming in lake
    event_type text(30),        --e.g. swimming
    event_subtype text(30)      --e.g. lap_swimming
);
''',
    "event_swimming":
'''
CREATE TABLE event_swimming(
    event_swimming_id integer primary key AUTOINCREMENT,
    f_id integer,             --File, the dataset belongs to
    event_timestamp datetime,  --time, event was recorded
    start_time datetime,       --time, event was started
    swim_stroke text(30),      --breast stroke, back stroke etc.
    total_calories integer,    --calculated calories for this lap
    total_elapsed_time float,  --time for this lap
    total_strokes integer,     --strokes for this lap
    distance integer
)
'''
}