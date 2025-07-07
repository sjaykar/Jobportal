CREATE DATABASE IF NOT EXISTS accorian_jobs;
USE accorian_jobs;

CREATE TABLE IF NOT EXISTS accorian_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title    VARCHAR(100)    NOT NULL,
    category ENUM('tech','non-tech','other') NOT NULL,
    location VARCHAR(100)    NOT NULL,
    openings INT             NOT NULL,
    logo_url VARCHAR(255),
    company  VARCHAR(100)    NOT NULL DEFAULT 'Accorian'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS applications (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    job_id     INT            NOT NULL,
    name       VARCHAR(100)   NOT NULL,
    email      VARCHAR(100)   NOT NULL,
    applied_at TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
) ENGINE=InnoDB;
