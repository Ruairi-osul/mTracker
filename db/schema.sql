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
    data_description TEXT,
    category VARCHAR(150) NOT NULL
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
    dob DATE,
    cull_date DATE,
    is_done INT DEFAULT 1,
    group_id INT NOT NULL,
    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE
);


CREATE TABLE datasets(
    id INT PRIMARY KEY AUTO_INCREMENT,
    mouse_id INT NOT NULL,
    session_type_id INT NOT NULL,
    data_type_id INT NOT NULL,
    FOREIGN KEY (session_type_id)
        REFERENCES session_types(id)
        ON DELETE CASCADE,
    FOREIGN KEY (mouse_id)
        REFERENCES mice(id)
        ON DELETE CASCADE,
    FOREIGN KEY (data_type_id)
        REFERENCES data_types(id)
        ON DELETE CASCADE
);
ALTER TABLE `datasets` 
    ADD UNIQUE `unique_datasets`(`mouse_id`, `session_type_id`, `data_type_id`);

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
    dataset_id INT NOT NULL,
    neuron_id INT NOT NULL,
    timepoint_sec DOUBLE NOT NULL,
    activity_value DOUBLE,
    FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE,
    FOREIGN KEY (neuron_id)
        REFERENCES neurons(id)
        ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, neuron_id, timepoint_sec)
);

CREATE TABLE images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_name VARCHAR(150),
    image_path VARCHAR(150) NOT NULL,
    mouse_id INT NOT NULL,
    FOREIGN KEY (mouse_id)
        REFERENCES mice(id)
        ON DELETE CASCADE
);

CREATE TABLE events (
    dataset_id INT NOT NULL,
    timepoint_sec DOUBLE NOT NULL,
    FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, timepoint_sec)
);

CREATE TABLE continuous_data (
    dataset_id INT NOT NULL,
    timepoint_sec DOUBLE NOT NULL,
    data_value DOUBLE,
    FOREIGN KEY (dataset_id)
        REFERENCES datasets(id)
        ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, timepoint_sec)
);


