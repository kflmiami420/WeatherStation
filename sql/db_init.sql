CREATE USER 'weatherstation-admin'@'localhost' IDENTIFIED BY 'adminpassword';
CREATE USER 'weatherstation-web'@'localhost' IDENTIFIED BY 'webpassword';
CREATE USER 'weatherstation-sensor'@'localhost' IDENTIFIED BY 'sensorpassword';

CREATE DATABASE weatherstation;

GRANT ALL PRIVILEGES ON weatherstation.* to 'weatherstation-admin'@'localhost' WITH GRANT OPTION;
GRANT SELECT, INSERT, UPDATE, DELETE ON weatherstation.* TO 'weatherstation-web'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON weatherstation.* TO 'weatherstation-sensor'@'localhost';
FLUSH PRIVILEGES;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE SCHEMA IF NOT EXISTS `weatherstation` DEFAULT CHARACTER SET utf8mb4;
USE `weatherstation`;
    -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Table `weatherstation`.`history` - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

CREATE TABLE IF NOT EXISTS `weatherstation`.`history` (
        `currentdatetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `min_temp_dht` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_temp_dht` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_temp_dht` DECIMAL(10, 3) NULL DEFAULT NULL,
        `min_hum` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_hum` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_hum` DECIMAL(10, 3) NULL DEFAULT NULL,
        `min_temp_bmp` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_temp_bmp` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_temp_bmp` DECIMAL(10, 3) NULL DEFAULT NULL,
        `min_press` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_press` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_press` DECIMAL(10, 3) NULL DEFAULT NULL,
        `min_UV` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_UV` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_UV` DECIMAL(10, 3) NULL DEFAULT NULL,
        `min_wind` DECIMAL(10, 3) NULL DEFAULT NULL,
        `max_wind` DECIMAL(10, 3) NULL DEFAULT NULL,
        `avg_wind` DECIMAL(10, 3) NULL DEFAULT NULL,
        PRIMARY KEY (`currentdatetime`)
    ) ENGINE = InnoDB 
    DEFAULT CHARACTER SET = utf8mb4;
    -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Table `weatherstation`.`sensordata` - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    CREATE TABLE IF NOT EXISTS `weatherstation`.`sensordata` (
        `currentdatetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `temperature_dht` DECIMAL(10, 3) NULL DEFAULT NULL,
        `humidity_dht` DECIMAL(10, 3) NULL DEFAULT NULL,
        `temperature_bmp` DECIMAL(10, 3) NULL DEFAULT NULL,
        `pressure_bmp` DECIMAL(10, 3) NULL DEFAULT NULL,
        `UV_si1145` DECIMAL(10, 3) NULL DEFAULT NULL,
        `windspeed` DECIMAL(10, 3) NULL DEFAULT NULL,
        PRIMARY KEY (`currentdatetime`)
    ) ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8mb4;
    -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Table `weatherstation`.`users` - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    CREATE TABLE IF NOT EXISTS `weatherstation`.`users` (
        `username` VARCHAR(45) NOT NULL,
        `email` VARCHAR(100) NULL DEFAULT NULL,
        `password` VARCHAR(100) NULL DEFAULT NULL,
        `unit_selection` CHAR(3) NULL DEFAULT 'kmh',
        `postcode` VARCHAR(45) NULL DEFAULT NULL,
        `country` VARCHAR(45) NULL DEFAULT NULL,
        `frequency` INT(11) NULL DEFAULT '10',
        `active` INT(11) NULL DEFAULT '0',
        PRIMARY KEY (`username`),
        UNIQUE INDEX `email_UNIQUE` (`email` ASC)
    ) ENGINE = InnoDB 
    DEFAULT CHARACTER SET = utf8mb4;
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO `weatherstation`.`history` (`currentdatetime`, `min_temp_dht`, `max_temp_dht`, `avg_temp_dht`, `min_hum`, `max_hum`, `avg_hum`, `min_temp_bmp`, `max_temp_bmp`, `avg_temp_bmp`, `min_press`, `max_press`, `avg_press`, `min_UV`, `max_UV`, `avg_UV`, `min_wind`, `max_wind`, `avg_wind`) VALUES (SUBDATE(CURDATE(),5), '10.000', '15.000', '12.000', '25.000', '75.000', '50.000', '10.000', '15.000', '12.000', '1010.000', '1027.000', '1020.000', '0.000', '3.000', '1.000', '0.000', '13.200', '10.100');
INSERT INTO `weatherstation`.`history` (`currentdatetime`, `min_temp_dht`, `max_temp_dht`, `avg_temp_dht`, `min_hum`, `max_hum`, `avg_hum`, `min_temp_bmp`, `max_temp_bmp`, `avg_temp_bmp`, `min_press`, `max_press`, `avg_press`, `min_UV`, `max_UV`, `avg_UV`, `min_wind`, `max_wind`, `avg_wind`) VALUES (SUBDATE(CURDATE(),4), '10.000', '15.000', '12.000', '25.000', '75.000', '50.000', '10.000', '15.000', '12.000', '1010.000', '1027.000', '1020.000', '0.000', '3.000', '1.000', '0.000', '13.200', '10.100');
INSERT INTO `weatherstation`.`history` (`currentdatetime`, `min_temp_dht`, `max_temp_dht`, `avg_temp_dht`, `min_hum`, `max_hum`, `avg_hum`, `min_temp_bmp`, `max_temp_bmp`, `avg_temp_bmp`, `min_press`, `max_press`, `avg_press`, `min_UV`, `max_UV`, `avg_UV`, `min_wind`, `max_wind`, `avg_wind`) VALUES (SUBDATE(CURDATE(),3), '10.000', '15.000', '12.000', '25.000', '75.000', '50.000', '10.000', '15.000', '12.000', '1010.000', '1027.000', '1020.000', '0.000', '3.000', '1.000', '0.000', '13.200', '10.100');
INSERT INTO `weatherstation`.`history` (`currentdatetime`, `min_temp_dht`, `max_temp_dht`, `avg_temp_dht`, `min_hum`, `max_hum`, `avg_hum`, `min_temp_bmp`, `max_temp_bmp`, `avg_temp_bmp`, `min_press`, `max_press`, `avg_press`, `min_UV`, `max_UV`, `avg_UV`, `min_wind`, `max_wind`, `avg_wind`) VALUES (SUBDATE(CURDATE(),2), '10.000', '15.000', '12.000', '25.000', '75.000', '50.000', '10.000', '15.000', '12.000', '1010.000', '1027.000', '1020.000', '0.000', '3.000', '1.000', '0.000', '13.200', '10.100');
INSERT INTO `weatherstation`.`history` (`currentdatetime`, `min_temp_dht`, `max_temp_dht`, `avg_temp_dht`, `min_hum`, `max_hum`, `avg_hum`, `min_temp_bmp`, `max_temp_bmp`, `avg_temp_bmp`, `min_press`, `max_press`, `avg_press`, `min_UV`, `max_UV`, `avg_UV`, `min_wind`, `max_wind`, `avg_wind`) VALUES (SUBDATE(CURDATE(),1), '10.000', '15.000', '12.000', '25.000', '75.000', '50.000', '10.000', '15.000', '12.000', '1010.000', '1027.000', '1020.000', '0.000', '3.000', '1.000', '0.000', '13.200', '10.100');