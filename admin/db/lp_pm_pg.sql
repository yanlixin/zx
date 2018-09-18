drop table PM_Roles;
drop table PM_R_Documents;
drop table PM_DocumentTeamMembers ;
drop table PM_DevliverableTeamMembers ;
drop table PM_ActivityTeamMembers;
drop table PM_TaskTeamMembers;
drop table PM_Activities;
drop table PM_Documents;
drop table PM_Deliverables;
drop table PM_TeamMembers;
drop table PM_Tasks;

CREATE TABLE PM_Projects (
ProjectID  UUID NOT NULL ,
ProjectNo VARCHAR(64) ,
ProjectName VARCHAR(512) NOT NULL DEFAULT 'NULL' ,
ProjectDesc VARCHAR(1024) ,
Remark VARCHAR(1024) ,
Memo VARCHAR(1024) ,
ScheduledStartDate DATE ,
ScheduledEndDate DATE ,
ActualStartDate DATE ,
ActualEndDate DATE ,
ExtraData XML ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (ProjectID)
);

CREATE TABLE PM_Tasks (
TaskID  UUID ,
ProjectID UUID NOT NULL ,
TaskPID UUID NOT NULL DEFAULT 0 ,
TaskNo VARCHAR(64) NOT NULL DEFAULT 'NULL' ,
TaskName VARCHAR(128) NOT NULL DEFAULT 'NULL' ,
TaskDesc VARCHAR(1024) ,
Memo VARCHAR(1024) ,
ScheduledStartDate DATE ,
ScheduledEndDate DATE ,
ActualStartDate DATE ,
EndStartDate DATE ,
IsCritical BOOLEAN ,
IsModifiable BOOLEAN ,
Weight DECIMAL(6,4) ,
ProgressPercentage DECIMAL(6,4) ,
ExtraData XML ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (TaskID)
);
COMMENT ON TABLE PM_Tasks IS 'WBS 一级:测绘,评估,拆迁,政府,审计,二级:标段,三级:村\户';

CREATE TABLE PM_TeamMembers (
TeamMemberID  UUID ,
ProjectID UUID NOT NULL ,
UserID UUID ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (TeamMemberID)
);

CREATE TABLE PM_Deliverables (
DeliverableID  UUID ,
ProjetcID UUID NOT NULL ,
DeliverableName VARCHAR(128) ,
DeliverableQty DECIMAL(8,2) ,
ScheduledDeliveryDate DATE ,
ScheduledStardDate DATE ,
ScheduledEndDate DATE ,
ActualStartDate DATE ,
ActualEndDate DATE ,
IsModifiable BOOLEAN ,
ExtraData XML ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (DeliverableID)
);

CREATE TABLE PM_Documents (
DocID  UUID ,
ProjectID UUID NOT NULL ,
Title VARCHAR(1024) ,
Desc VARCHAR(1024) ,
Memo VARCHAR(1024) ,
Summary VARCHAR(1024) ,
CategoryID SMALLINT ,
FileTypeID SMALLINT ,
LastedVersion VARCHAR(32) ,
Preview VARBIT ,
ExtraData XML ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (DocID)
);

CREATE TABLE PM_Activities (
ActivatID  UUID ,
ProjectID UUID NOT NULL ,
TaskID UUID ,
ActivateNo VARCHAR(64) NOT NULL DEFAULT 'NULL' ,
ActivateName VARCHAR(128) NOT NULL DEFAULT 'NULL' ,
ActivateDesc VARCHAR(1024) ,
Memo VARCHAR(1024) ,
ScheduleStartDate DATE ,
ScheduleEndDate DATE ,
ActualStartDate DATE ,
ActualEndDate DATE ,
IsModeifiable BOOLEAN ,
Weight DECIMAL(6,4) ,
ProgressPercentage DECIMAL(6,4) ,
ExtraData XML ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate UUID ,
LastedByUserID TIMESTAMP ,
PRIMARY KEY (ActivatID)
);

CREATE TABLE PM_TaskTeamMembers (
TaskTeamMemeberID  UUID NOT NULL ,
TaskID UUID ,
TeamMemberID UUID ,
IsManager BOOLEAN ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (TaskTeamMemeberID)
);

CREATE TABLE PM_ActivityTeamMembers (
ActivityTeamMemberID  UUID NOT NULL ,
ActivatID UUID ,
TeamMemberID UUID ,
IsManager BOOLEAN ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (ActivityTeamMemberID)
);

CREATE TABLE PM_DevliverableTeamMembers (
DevliverableTeamMemberID  UUID NOT NULL ,
DeliverableID UUID ,
TeamMemberID UUID ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (DevliverableTeamMemberID)
);

CREATE TABLE PM_DocumentTeamMembers (
DocTeamMemberID  UUID ,
DocID UUID ,
TeamMemberID UUID ,
IsManager BOOLEAN ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (DocTeamMemberID)
);

CREATE TABLE PM_R_Documents (
R_DocID  UUID ,
DocID UUID ,
AssociateItemDefinitionID INTEGER ,
AssociateItemID UUID ,
PRIMARY KEY (R_DocID)
);

CREATE TABLE PM_Roles (
RoleID  UUID ,
ProjectID UUID NOT NULL ,
RoleName VARCHAR(64) ,
RoleDesc VARCHAR(512) ,
Memo VARCHAR(1024) ,
Remark VARCHAR(512) ,
Permission VARCHAR(128) ,
RecordStatus SMALLINT ,
CreatedDate TIMESTAMP ,
CreatedByUserID UUID ,
LastedDate TIMESTAMP ,
LastedByUserID UUID ,
PRIMARY KEY (RoleID)
);

ALTER TABLE PM_Tasks ADD FOREIGN KEY (ProjectID) REFERENCES PM_Projects (ProjectID);
ALTER TABLE PM_TeamMembers ADD FOREIGN KEY (ProjectID) REFERENCES PM_Projects (ProjectID);
ALTER TABLE PM_Deliverables ADD FOREIGN KEY (ProjetcID) REFERENCES PM_Projects (ProjectID);
ALTER TABLE PM_Documents ADD FOREIGN KEY (ProjectID) REFERENCES PM_Projects (ProjectID);
ALTER TABLE PM_Activities ADD FOREIGN KEY (ProjectID) REFERENCES PM_Projects (ProjectID);
ALTER TABLE PM_Activities ADD FOREIGN KEY (TaskID) REFERENCES PM_Tasks (TaskID);
ALTER TABLE PM_TaskTeamMembers ADD FOREIGN KEY (TaskID) REFERENCES PM_Tasks (TaskID);
ALTER TABLE PM_ActivityTeamMembers ADD FOREIGN KEY (ActivatID) REFERENCES PM_Activities (ActivatID);
ALTER TABLE PM_DevliverableTeamMembers ADD FOREIGN KEY (DeliverableID) REFERENCES PM_Deliverables (DeliverableID);
ALTER TABLE PM_DocumentTeamMembers ADD FOREIGN KEY (DocID) REFERENCES PM_Documents (DocID);
ALTER TABLE PM_R_Documents ADD FOREIGN KEY (DocID) REFERENCES PM_Documents (DocID);
ALTER TABLE PM_Roles ADD FOREIGN KEY (ProjectID) REFERENCES PM_Projects (ProjectID);