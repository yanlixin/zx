DROP TABLE R_Permissions_Roles ;
DROP TABLE Permissions ;
DROP TABLE R_Users_Roles; 
DROP TABLE Roles;
DROP TABLE Users;

CREATE TABLE "Users" (
"UserID" UUID NOT NULL ,
"UserName" VARCHAR(64) NOT NULL ,
"LoginName" VARCHAR(64) NOT NULL ,
"LoginPwd" VARCHAR(512) NOT NULL ,
"Salt" VARCHAR(120) ,
"Mobile" VARCHAR(32) ,
"EMail" VARCHAR(128) ,
"UserDesc" VARCHAR(512) ,
"Remark" VARCHAR(512) ,
"IsMaster" BOOLEAN ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" UUID ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" UUID ,
PRIMARY KEY ("UserID")
);

CREATE TABLE "Roles" (
"RoleID" UUID NOT NULL ,
"RoelName" VARCHAR(64) ,
"RoleDesc" VARCHAR(512) ,
"IsSys" BOOLEAN ,
"SortIndex" VARCHAR ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" UUID ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" UUID ,
PRIMARY KEY ("RoleID")
);

CREATE TABLE "R_Users_Roles" (
"RUserRoleID" UUID NOT NULL ,
"UserID" UUID ,
"RoleID" UUID ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" UUID ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" UUID ,
PRIMARY KEY ("RUserRoleID")
);

CREATE TABLE "Permissions" (
"PermID" UUID NOT NULL ,
"PermKey" VARCHAR(128) NOT NULL DEFAULT 'NULL' ,
"PermName" VARCHAR(64) NOT NULL DEFAULT 'NULL' ,
"PermDesc" VARCHAR(512) ,
"PermGroup" VARCHAR(64) NOT NULL DEFAULT 'NULL' ,
"IsSys" BOOLEAN ,
"CreatedByUserID" UUID ,
"CreatedDate" TIMESTAMP ,
PRIMARY KEY ("PermID")
);

CREATE TABLE "R_Permissions_Roles" (
"RPermRoleID" UUID NOT NULL ,
"RoleID" UUID ,
"PermID" UUID ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" UUID ,
PRIMARY KEY ("RPermRoleID")
);

ALTER TABLE "R_Users_Roles" ADD FOREIGN KEY ("UserID") REFERENCES "Users" ("UserID");
ALTER TABLE "R_Users_Roles" ADD FOREIGN KEY ("RoleID") REFERENCES "Roles" ("RoleID");
ALTER TABLE "R_Permissions_Roles" ADD FOREIGN KEY ("RoleID") REFERENCES "Roles" ("RoleID");
ALTER TABLE "R_Permissions_Roles" ADD FOREIGN KEY ("PermID") REFERENCES "Permissions" ("PermID");
