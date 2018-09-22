/*drop table "PM_Roles";
drop table "PM_R_Docs";
drop table "PM_DocTeamMembers" ;
drop table "PM_DevliverableTeamMembers" ;
drop table "PM_ActivityTeamMembers";
drop table "PM_TaskTeamMembers";
drop table "PM_Activities";
drop table "PM_Docs";
drop table "PM_DocCategories";
drop table "PM_Deliverables";
drop table "PM_TeamMembers";
drop table "PM_Tasks";
*/

CREATE TABLE "PM_Projects" (
"ProjectID" UUID NOT NULL ,
"ProjectNo" VARCHAR(64) ,
"ProjectName" VARCHAR(512) NOT NULL ,
"ProjectFullName" VARCHAR(512) NOT NULL ,
"ProjectDesc" VARCHAR(1024) ,
"Remark" VARCHAR(1024) ,
"Memo" VARCHAR(1024) ,
"ScheduledStartDate" DATE ,
"ScheduledEndDate" DATE ,
"ActualStartDate" DATE ,
"ActualEndDate" DATE ,
"Client" VARCHAR(1024) ,
"ProjectManger" VARCHAR(1024) ,
"ExtraData" JSONB ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("ProjectID")
);

CREATE TABLE "PM_Tasks" (
"TaskID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"TaskPID" UUID ,
"TaskNo" VARCHAR(64) ,
"TaskName" VARCHAR(128) NOT NULL ,
"TaskDesc" VARCHAR(1024) ,
"Memo" VARCHAR(1024) ,
"ScheduledStartDate" DATE ,
"ScheduledEndDate" DATE ,
"ActualStartDate" DATE ,
"EndStartDate" DATE ,
"IsCritical" BOOLEAN ,
"IsModifiable" BOOLEAN ,
"Weight" DECIMAL(6,4) ,
"ProgressPercentage" DECIMAL(6,4) ,
"ExtraData" JSONB ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("TaskID")
);
COMMENT ON TABLE "PM_Tasks" IS 'WBS 一级:测绘,评估,拆迁,政府,审计,二级:标段,三级:村\户';

CREATE TABLE "PM_TeamMembers" (
"TeamMemberID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"UserID" BIGINT ,
"LoginName" VARCHAR(64) ,
"IsManager" BOOLEAN ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
"Desc" VARCHAR(1024) ,
PRIMARY KEY ("TeamMemberID")
);

CREATE TABLE "PM_Deliverables" (
"DeliverableID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"DeliverableNo" VARCHAR(64) ,
"DeliverableName" VARCHAR(128) ,
"DeliverableQty" DECIMAL(8,2) ,
"DeliverableDesc" VARCHAR(1024) ,
"ScheduledDeliveryDate" DATE ,
"ScheduledStardDate" DATE ,
"ScheduledEndDate" DATE ,
"ActualStartDate" DATE ,
"ActualEndDate" DATE ,
"IsModifiable" BOOLEAN ,
"Memo" VARCHAR(1024) ,
"Remark" VARCHAR(1024) ,
"ExtraData" JSONB ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("DeliverableID")
);

CREATE TABLE "PM_Docs" (
"DocID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"DocCatID" UUID ,
"DocNo" VARCHAR(64) ,
"Title" VARCHAR(1024) ,
"FullName" VARCHAR(1024) ,
"Alias" VARCHAR(1024) ,
"Desc" VARCHAR(1024) ,
"Memo" VARCHAR(1024) ,
"Summary" VARCHAR(1024) ,
"FileType" VARCHAR(16) ,
"LastedVersion" VARCHAR(32) ,
"Preview" BYTEA ,
"FileData" BYTEA ,
"ExtraData" JSONB ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("DocID")
);

CREATE TABLE "PM_Activities" (
"ActivatID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"TaskID" UUID ,
"ActivateNo" VARCHAR(64) ,
"ActivateName" VARCHAR(128) NOT NULL ,
"ActivateDesc" VARCHAR(1024) ,
"Memo" VARCHAR(1024) ,
"ScheduleStartDate" DATE ,
"ScheduleEndDate" DATE ,
"ActualStartDate" DATE ,
"ActualEndDate" DATE ,
"IsModeifiable" BOOLEAN ,
"Weight" DECIMAL(6,4) ,
"ProgressPercentage" DECIMAL(6,4) ,
"ExtraData" JSONB ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" BIGINT ,
"LastedByUserID" TIMESTAMP ,
PRIMARY KEY ("ActivatID")
);

CREATE TABLE "PM_TaskTeamMembers" (
"TaskTeamMemeberID"  SERIAL NOT NULL ,
"TaskID" UUID NOT NULL ,
"TeamMemberID" UUID ,
"IsManager" BOOLEAN ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("TaskTeamMemeberID")
);

CREATE TABLE "PM_ActivityTeamMembers" (
"ActivityTeamMemberID" UUID NOT NULL ,
"ActivatID" UUID NOT NULL ,
"TeamMemberID" BIGINT ,
"IsManager" BOOLEAN ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("ActivityTeamMemberID")
);

CREATE TABLE "PM_DevliverableTeamMembers" (
"DevliverableTeamMemberID" UUID NOT NULL ,
"DeliverableID" UUID ,
"TeamMemberID" BIGINT ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("DevliverableTeamMemberID")
);

CREATE TABLE "PM_DocTeamMembers" (
"DocTeamMemberID" UUID NOT NULL ,
"DocID" UUID ,
"TeamMemberID" UUID ,
"IsManager" BOOLEAN ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("DocTeamMemberID")
);

CREATE TABLE "PM_R_Docs" (
"R_DocID" UUID NOT NULL ,
"DocID" UUID ,
"AssociateItemDefinitionID" INTEGER ,
"AssociateItemID" BIGINT ,
PRIMARY KEY ("R_DocID")
);

CREATE TABLE "PM_Roles" (
"RoleID" UUID NOT NULL ,
"ProjectID" UUID NOT NULL ,
"RoleName" VARCHAR(64) ,
"RoleDesc" VARCHAR(512) ,
"Memo" VARCHAR(1024) ,
"Remark" VARCHAR(512) ,
"Permission" VARCHAR(128) ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"CreatedByUserID" BIGINT ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" BIGINT ,
PRIMARY KEY ("RoleID")
);

CREATE TABLE "PM_DocCategories" (
"DocCatID" UUID NOT NULL ,
"ProjectID" UUID /* 对否关联项目为可选项 */,
"CatName" VARCHAR(64) NOT NULL ,
"CatDesc" VARCHAR(1024) ,
"ExtraData" JSONB ,
"Preview" OID ,
"IsRequired" BOOLEAN NOT NULL ,
"RecordStatus" SMALLINT ,
"CreatedDate" TIMESTAMP ,
"LastedDate" TIMESTAMP ,
"LastedByUserID" INTEGER ,
"CratedByUserID" INTEGER ,
PRIMARY KEY ("DocCatID")
);
COMMENT ON COLUMN "PM_DocCategories"."ProjectID" IS '对否关联项目为可选项';

ALTER TABLE "PM_Tasks" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");
ALTER TABLE "PM_TeamMembers" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");
ALTER TABLE "PM_Deliverables" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");
ALTER TABLE "PM_Docs" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");
ALTER TABLE "PM_Docs" ADD FOREIGN KEY ("DocCatID") REFERENCES "PM_DocCategories" ("DocCatID");
ALTER TABLE "PM_Activities" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");
ALTER TABLE "PM_Activities" ADD FOREIGN KEY ("TaskID") REFERENCES "PM_Tasks" ("TaskID");
ALTER TABLE "PM_TaskTeamMembers" ADD FOREIGN KEY ("TaskID") REFERENCES "PM_Tasks" ("TaskID");
ALTER TABLE "PM_ActivityTeamMembers" ADD FOREIGN KEY ("ActivatID") REFERENCES "PM_Activities" ("ActivatID");
ALTER TABLE "PM_DevliverableTeamMembers" ADD FOREIGN KEY ("DeliverableID") REFERENCES "PM_Deliverables" ("DeliverableID");
ALTER TABLE "PM_DocTeamMembers" ADD FOREIGN KEY ("DocID") REFERENCES "PM_Docs" ("DocID");
ALTER TABLE "PM_R_Docs" ADD FOREIGN KEY ("DocID") REFERENCES "PM_Docs" ("DocID");
ALTER TABLE "PM_Roles" ADD FOREIGN KEY ("ProjectID") REFERENCES "PM_Projects" ("ProjectID");