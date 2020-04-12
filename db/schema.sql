DROP DATABASE IF EXISTS mtracker;
CREATE DATABASE mtracker;
USE mtracker;

CREATE TABLE experiments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exp_name VARCHAR(150) UNIQUE NOT NULL,
    exp_description TEXT
);

CREATE TABLE session_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_name VARCHAR(100) NOT NULL,
    session_description TEXT NOT NULL
);

CREATE TABLE surgery_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    surgery_name VARCHAR(100) NOT NULL,
    surgery_description TEXT
);

CREATE TABLE event_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(100) NOT NULL,
    event_description TEXT
);

CREATE TABLE trajectory_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    trajectory_name VARCHAR(100) NOT NULL,
    trajectory_description VARCHAR(100)
);

CREATE TABLE groups (
    id INT PRIMARY KEY AUTO_INCREMENT,
    experiment_id INT NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    genotype VARCHAR(50) NOT NULL,
    group_description TEXT,
    FOREIGN KEY (experiment_id)
        REFERENCES experiments(id)
        ON DELETE CASCADE
);

CREATE TABLE data_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_name VARCHAR(100) NOT NULL,
    data_description TEXT
);

CREATE TABLE group_sessiontypes (
    group_id INT NOT NULL,
    sessiontype_id INT NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    FOREIGN KEY (sessiontype_id)
        REFERENCES session_types(id)
        ON DELETE CASCADE,
    PRIMARY KEY (group_id, sessiontype_id)
);

CREATE TABLE group_datatypes(
    group_id INT NOT NULL,
    datatype_id INT NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    FOREIGN KEY (datatype_id)
        REFERENCES data_types(id)
        ON DELETE CASCADE,
    PRIMARY KEY(group_id, datatype_id)
);

CREATE TABLE group_surgerytypes (
    group_id INT NOT NULL,
    surgery_id INT NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    FOREIGN KEY (surgery_id)
        REFERENCES surgery_types(id)
        ON DELETE CASCADE,
    PRIMARY KEY (group_id, surgery_id)
);

CREATE TABLE mice (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mouse_name VARCHAR(100) NOT NULL,
    is_male INT NOT NULL DEFAULT 1,
    group_id INT NOT NULL,
    dob DATE,
    cull_date DATE,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE
);

CREATE TABLE histology (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mouse_id INT NOT NULL,
    image_name VARCHAR(150),
    image_path VARCHAR(150) NOT NULL,
    FOREIGN KEY (mouse_id)
        REFERENCES mice(id)
        ON DELETE CASCADE
);

CREATE TABLE experimental_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_type_id INT NOT NULL,
    mouse_id INT NOT NULL,
    FOREIGN KEY (session_type_id)
        REFERENCES session_types(id)
        ON DELETE CASCADE,
    FOREIGN KEY (mouse_id)
        REFERENCES mice(id)
        ON DELETE CASCADE
);

CREATE TABLE experiment_events (
    id INT PRIMARY KEY NOT NULL,
    experimental_session_id INT NOT NULL,
    event_type_id INT NOT NULL,
    FOREIGN KEY (experimental_session_id)
        REFERENCES experimental_sessions(id)
        ON DELETE CASCADE
);

CREATE TABLE neurons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mouse_id INT NOT NULL,
    x_pos DOUBLE NOT NULL,
    y_pos DOUBLE NOT NULL,
    FOREIGN KEY (mouse_id)
        REFERENCES mice(id)
        ON DELETE CASCADE
);

CREATE TABLE neuronal_activity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    experimental_session INT NOT NULL,
    neuron_id INT NOT NULL,
    activity_value DOUBLE,
    FOREIGN KEY (experimental_session)
        REFERENCES experimental_sessions(id)
        ON DELETE CASCADE,
    FOREIGN KEY (neuron_id)
        REFERENCES neurons(id)
        ON DELETE CASCADE
);
