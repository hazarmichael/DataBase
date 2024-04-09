
create database projectdb; 
use projectdb; 

Create table Customer (
	CustomerID varchar(20), Cname varchar(30), DateOfBirth date , ContactNumber varchar(20), Email varchar(50),
	primary key (CustomerID)

	)
    
	Create table own_car (
	CarID varchar(20), Model varchar(20), ManufactureYear YEAR  , RegistrationNumber INTEGER, CustomerID varchar(20) NOT NULL,
	primary key (CarID),
	Foreign key (CustomerID) REFERENCES Customer (CustomerID) ON DELETE NO ACTION 
	)
    
CREATE TABLE have_Insurancepolicy (
    PolicyNo INT,
    StartDate DATE,
    EndDate DATE,
    CoverageType VARCHAR(20),
    PremiumAmount DOUBLE,
    CarID VARCHAR(20),
    PRIMARY KEY (PolicyNo),
    FOREIGN KEY (CarID) REFERENCES own_car (CarID)
);

CREATE TABLE pay_payment (
    PaymentNo INT,
    Amount DOUBLE,
    PaymentDate DATE,
    PaymentMethod VARCHAR(30),
    CarID VARCHAR(20) NOT NULL,
    PRIMARY KEY (PaymentNo),
    FOREIGN KEY (CarID) REFERENCES own_car (CarID) ON DELETE NO ACTION
);
CREATE TABLE CoveredPerson (
    CoveredPersonID VARCHAR(20),
    CoveredName VARCHAR(20),
    PolicyNo INT,
    PRIMARY KEY (PolicyNo, CoveredPersonID),
    FOREIGN KEY (PolicyNo) REFERENCES have_insurancepolicy (PolicyNo) ON DELETE CASCADE
);

################### we manually did the paumentNO and Insurance no to be auto incremented 
    
    
########just to test the dataset and delete all of its contents 
SET SQL_SAFE_UPDATES = 0;
DELETE FROM Customer;
DELETE FROM own_car; 
DELETE FROM have_Insurancepolicy; 
DELETE FROM pay_payment; 
DELETE FROM CoveredPerson; 
    
SET SQL_SAFE_UPDATES = 1;
