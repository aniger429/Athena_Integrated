-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema Athena
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Athena
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Athena` DEFAULT CHARACTER SET utf8 ;
USE `Athena` ;

-- -----------------------------------------------------
-- Table `Athena`.`Username`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Athena`.`Username` (
  `idUsername` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `numTweets` INT NOT NULL DEFAULT 0,
  `numMentions` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`idUsername`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `idUsername_UNIQUE` (`idUsername` ASC))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
