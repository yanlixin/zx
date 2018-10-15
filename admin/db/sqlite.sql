CREATE TABLE 'Cities' (
'cityid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'provid' INTEGER DEFAULT NULL REFERENCES 'Provinces' ('provid'),
'cityname' TEXT(64) DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL
);

CREATE TABLE 'Provinces' (
'provid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'provname' TEXT(64) DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL
);

CREATE TABLE 'Districts' (
'districtid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'cityid' INTEGER DEFAULT NULL REFERENCES 'Cities' ('cityid'),
'districtname' TEXT(64) DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL
);

CREATE TABLE 'Schools' (
'schoolid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'districtid' INTEGER DEFAULT NULL,
'schoolname' TEXT(128) DEFAULT NULL,
'schooldesc' TEXT(1024) DEFAULT NULL,
'addr' TEXT(126) DEFAULT NULL,
'tuition' TEXT(64) DEFAULT NULL,
'features' TEXT(1024) DEFAULT NULL,
'phone' TEXT(64) DEFAULT NULL,
'intro' TEXT(1024) DEFAULT NULL,
'team' TEXT(1024) DEFAULT NULL,
'founded' TEXT(32) DEFAULT NULL,
'age' TEXT(63) DEFAULT NULL,
'scale' TEXT(64) DEFAULT NULL,
'population' TEXT(32) DEFAULT NULL,
'duration' TEXT(32) DEFAULT NULL,
'foreignduration' TEXT(1024) DEFAULT NULL,
'schoolbus' TEXT(16) DEFAULT NULL,
'cramclass' TEXT DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL,
'lastupdatedbydate' TEXT DEFAULT NULL,
'lastupdatedbymanagerid' INTEGER DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL,
'catid' INTEGER DEFAULT NULL,
'catname' TEXT DEFAULT NULL,
'povid' INTEGER DEFAULT NULL,
'provnae' TEXT DEFAULT NULL,
'cityid' INTEGER DEFAULT NULL,
'cityname' TEXT DEFAULT NULL,
'districtname' TEXT DEFAULT NULL,
'img' TEXT DEFAULT NULL,
'thumb' TEXT DEFAULT NULL,
'isbest' INTEGER DEFAULT NULL,
'isnew' INTEGER DEFAULT NULL,
'ishot' INTEGER DEFAULT NULL,
'istopshow' INTEGER DEFAULT NULL,
'gradeid' INTEGER DEFAULT NULL,
'gradename' TEXT DEFAULT NULL,
'cbdid' INTEGER DEFAULT NULL,
'cbdname' TEXT DEFAULT NULL,
'lon' TEXT DEFAULT NULL,
'lat' TEXT DEFAULT NULL,
'shcoolpid' INTEGER DEFAULT NULL,
'isbilingual' INTEGER DEFAULT NULL
);

CREATE TABLE 'Users' (
'userid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'username' TEXT(64) DEFAULT NULL,
'loginname' TEXT(64) DEFAULT NULL,
'loginpwd' TEXT(64) DEFAULT NULL,
'mobile' TEXT(32) DEFAULT NULL,
'email' TEXT(64) DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydatetime' TEXT DEFAULT NULL,
'lastupdatedbydatetime' TEXT DEFAULT NULL,
'lasteupdatedbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'Managers' (
'managerid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'managername' TEXT(63) DEFAULT NULL,
'loginname' TEXT(64) DEFAULT NULL,
'loginpwd' TEXT(512) DEFAULT NULL,
'salt' TEXT DEFAULT NULL,
'mobile' TEXT(32) DEFAULT NULL,
'email' TEXT(64) DEFAULT NULL,
'desc' TEXT DEFAULT NULL,
'remark' TEXT DEFAULT NULL,
'ismaster' INTEGER DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL,
'lastupdatedbydate' TEXT DEFAULT NULL,
'lastupdatedbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'Categories' (
'catid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'catname' TEXT DEFAULT NULL,
'catdesc' TEXT DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL,
'typeid' INTEGER NOT NULL  DEFAULT 1,
'typename' TEXT NOT NULL  DEFAULT '学校'
);

CREATE TABLE 'Grades' (
'gradeid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'gradename' TEXT DEFAULT NULL,
'gradedesc' TEXT DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'schoolgalleries' (
'galleryid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'imagedesc' TEXT DEFAULT NULL,
'imagetitle' TEXT DEFAULT NULL,
'imagepath' TEXT DEFAULT NULL,
'isdefault' TEXT DEFAULT NULL,
'istopshow' TEXT DEFAULT NULL,
'isenable' TEXT DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createddate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'SmsCode' (
'smscodeid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'mobile' TEXT DEFAULT NULL,
'senddatetime' TEXT DEFAULT NULL,
'verifycode' TEXT DEFAULT NULL,
'hasverified' TEXT DEFAULT NULL,
'createdbydatetime' TEXT DEFAULT NULL
);

CREATE TABLE 'Roles' (
'roleid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'rolename' TEXT DEFAULT NULL,
'roledesc' TEXT DEFAULT NULL,
'IsSys' TEXT DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL,
'lastupdatedbydate' TEXT DEFAULT NULL,
'lastupdatedbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'R_Users_Roles' (
'ruserroleid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'managerid' INTEGER DEFAULT NULL REFERENCES 'Managers' ('managerid'),
'roleid' INTEGER DEFAULT NULL REFERENCES 'Roles' ('roleid'),
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' TEXT DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'lastupdatedbydate' TEXT DEFAULT NULL,
'lastupdatedbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'Permissions' (
'permid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'permuuid' TEXT DEFAULT NULL,
'permname' TEXT DEFAULT NULL,
'permdesc' TEXT DEFAULT NULL,
'permgroup' TEXT DEFAULT NULL,
'IsSys' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL,
'createdbydate' TEXT DEFAULT NULL
);

CREATE TABLE 'R_Permissions_Roles' (
'rpermroleid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'roleid' INTEGER DEFAULT NULL REFERENCES 'Roles' ('roleid'),
'permid' INTEGER DEFAULT NULL REFERENCES 'Permissions' ('permid'),
'createdbydate' TEXT DEFAULT NULL,
'createdbymanagerid' INTEGER DEFAULT NULL
);

CREATE TABLE 'new table' (
'id' TEXT DEFAULT NULL PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE 'CBDs' (
'cbdid' INTEGER DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'cbdname' TEXT DEFAULT NULL,
'cbddesc' TEXT DEFAULT NULL,
'lon' TEXT DEFAULT NULL,
'lat' TEXT DEFAULT NULL,
'districtid' INTEGER DEFAULT NULL REFERENCES 'Districts' ('districtid'),
'sortindex' INTEGER DEFAULT NULL
);

CREATE TABLE 'new table' (
'id' TEXT DEFAULT NULL PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE 'InterestClasses' (
'InterestClassID' INTEGER NOT NULL  DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'districtid' INTEGER DEFAULT NULL,
'InterestClassName' TEXT DEFAULT NULL,
'interestclassdesc' TEXT DEFAULT NULL,
'addr' TEXT DEFAULT NULL,
'new field' TEXT DEFAULT NULL
);

CREATE TABLE 'Shows' (
'showid' INTEGER NOT NULL  DEFAULT NULL PRIMARY KEY AUTOINCREMENT,
'showname' TEXT DEFAULT NULL,
'addr' TEXT DEFAULT NULL,
'begindate' TEXT DEFAULT NULL,
'enddate' TEXT DEFAULT NULL,
'price' NUMERIC(10,2) DEFAULT NULL,
'maxprice' NUMERIC(10,2) DEFAULT NULL,
'duration' TEXT DEFAULT NULL,
'districtid' INTEGER DEFAULT NULL,
'districtname' TEXT DEFAULT NULL,
'cityid' INTEGER DEFAULT NULL,
'cityname' TEXT DEFAULT NULL,
'provid' INTEGER DEFAULT NULL,
'provname' TEXT DEFAULT NULL,
'img' TEXT DEFAULT NULL,
'thumb' TEXT DEFAULT NULL,
'isbest' INTEGER DEFAULT NULL,
'isnew' INTEGER DEFAULT NULL,
'ishot' INTEGER DEFAULT NULL,
'istopshow' INTEGER DEFAULT NULL,
'cbdid' INTEGER DEFAULT NULL,
'cbdname' TEXT DEFAULT NULL,
'lon' TEXT DEFAULT NULL,
'lat' TEXT DEFAULT NULL,
'features' TEXT DEFAULT NULL,
'intro' TEXT DEFAULT NULL,
'catid' TEXT DEFAULT NULL,
'recordstatus' INTEGER DEFAULT NULL,
'catname' TEXT DEFAULT NULL,
'phone' TEXT DEFAULT NULL,
'showdesc' TEXT DEFAULT NULL,
'sortindex' INTEGER DEFAULT NULL
);