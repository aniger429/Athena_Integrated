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
  `username` VARCHAR(20) NOT NULL,
  `numTweets` INT NOT NULL DEFAULT 0,
  `numMentions` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`idUsername`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `idUsername_UNIQUE` (`idUsername` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Athena`.`Tweets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Athena`.`Tweets` (
  `idTweets` INT NOT NULL,
  `tweet` VARCHAR(140) NOT NULL,
  `dateCreated` DATETIME NOT NULL,
  `idUsername` INT NOT NULL,
  PRIMARY KEY (`idTweets`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Athena`.`Features`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Athena`.`Features` (
  `idTweets` INT NOT NULL,
  `favorite` INT NOT NULL,
  `retweet` INT NOT NULL,
  `location` VARCHAR(140) NOT NULL,
  `hashtags` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTweets`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Athena`.`Hashtags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Athena`.`Hashtags` (
  `idHashtag` INT NOT NULL AUTO_INCREMENT,
  `hashtag` VARCHAR(140) NOT NULL,
  PRIMARY KEY (`idHashtag`),
  UNIQUE INDEX `hashtag_UNIQUE` (`hashtag` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Athena`.`Data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Athena`.`Data` (
  `idData` INT NOT NULL AUTO_INCREMENT,
  `filename` VARCHAR(255) NOT NULL,
  `isClean` TINYINT(1) NOT NULL DEFAULT 0,
  `dateCreated` DATE NOT NULL,
  PRIMARY KEY (`idData`))
ENGINE = InnoDB
COMMENT = 'metadata about the data uploaded';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
