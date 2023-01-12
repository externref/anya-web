CREATE TABLE IF NOT EXISTS login_data (
    user_id BIGINT NOT NULL,
    session_id VARCHAR PRIMARY KEY NOT NULL,
    access_token VARCHAR,
    refresh_token VARCHAR,
    token_type VARCHAR
);

CREATE TABLE IF NOT EXISTS web_configs (
    bot_token VARCHAR,
    client_secret VARCHAR,
    client_id BIGINT,
    redirect VARCHAR
);
