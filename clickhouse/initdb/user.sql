CREATE TABLE default.user (
    id Int64,
    name String,
    last_name String,
    email String,
    birth_date Date,
    password String,
    gender UInt8,
    interests String,
    city String,
    age UInt8
)
ENGINE = MergeTree()
PARTITION BY (age,gender)
ORDER BY (age,gender);