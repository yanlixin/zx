
insert into Managers("managername","loginname","remark","loginpwd","salt","ismaster") values("master","master",'密码:111111',"pbkdf2:sha256:50000$rm07FeSe$013b1fac18f5da7354632805be8d978a45035628f8b3213ace35be782900c8d2","",1)
INSERT INTO "PM_DocCats"

insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("幼儿园","幼儿园",10000,0,0,0);
insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("小学","小学",10100,0,0,0);
insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("初中","初中",10200,0,0,0);
insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("高中","高中",10300,0,0,0);
insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("大学","大学",10400,0,0,0);
insert into Grades("gradename","gradedesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("培训机构","培训机构",10500,0,0,0);

insert into Categories("catname","catdesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("双语","双语",10000,0,0,0);
insert into Categories("catname","catdesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("国际","国际",10100,0,0,0);
insert into Categories("catname","catdesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("公立","公立",10200,0,0,0);
insert into Categories("catname","catdesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("民办(已备案)","民办(已备案)",10300,0,0,0);
insert into Categories("catname","catdesc","sortindex","recordstatus","createdbydate","createdbymanagerid") values("民办(未备案)","民办(未备案)",10400,0,0,0);



insert into Provinces("provname","sortindex") values("北京",110000);
insert into Provinces("provname","sortindex") values("上海",120000);
insert into Provinces("provname","sortindex") values("广东",130000);

insert into Cities("provid","cityname","sortindex") values(1,"北京",111000);

insert into Districts("cityid","districtname","sortindex") values(1,"朝阳",111001);
insert into Districts("cityid","districtname","sortindex") values(1,"海淀",111001);
insert into Districts("cityid","districtname","sortindex") values(1,"东城",111001);
insert into Districts("cityid","districtname","sortindex") values(1,"西城",111001);
