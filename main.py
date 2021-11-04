LoRaWAN Smart Watch Payload
V2.0.0

Document Revision Record
Version	Time	Description	Remark
V1.0.0	2020-05-11	Preliminary version	Jack
V2.0.0	2021-9-8	 Update health check data protocol	     Jack
			
1.Data frame
Description：
Header with fixed value BDBDBDBD
Message ID：Protocol id
Payload: Specific message content, size depending on message ID. The variables inside are all in little-endian mode
CK: Checksum , 1 byte. Buffer[N] indicates the data to be accumulated.
Ck_sum = 0	
For(i=0; i<N; i++)	
{
ck_sum = ck_sum + Buffer[i]
ck_sum = ck_sum % 0x100
}
Ck_sum = 0xFF – ck_sum
Return ck_sum

2.Device to Server Message
2.1 Uplink power info（MSGID=0XF6）
Payload contents
Byte offset	Format	Name	Scale	Unit	Description
2	u16	Bat_volt		-/-	Battery level
4	U32	Step_num			Number of steps
1	U8	Signal_strength			Signal strength
4	Int32	Timestamp			Time stamp in little-endian mode
Eg：bdbdbdbdf603009404000050cf084e5f2a
F6 --- MSGID
0300 --- Little-endian，0x0030 ) The battery level is 3 , and the reported value of battery 0-5 corresponds to 0%-100% (0% 20% 40% 60% 80% 100%);
94040000 ---  Little-endian，0x00000494, 1172 steps；
50 --- Signal strength 80%；
cf084e5f --- Little-endian, 0x5f4e08cf, after Unix timestamp conversion, the value is: 2020/9/1 16:39:43;
2a --- check code
2.2  Uplink GPS location （MSGID=0X03）
Payload contents
Byte offset	Format	Name	Scale	Unit	Description
8	Double	lon		-/-	longitude
8	Double	lat		　	latitude
1	U8	north_south			/*N or S*/
1	U8	east_west			/*E or W*/
1	U8	status			/*A or V*/
4	U32	Timestamp				Time stamp
eg：
bdbdbdbd0322fb20cb827a5c4021ea3e00a99536404e4541cf084e5f13
03 ---MSGID
22fb20cb827a5c40 --- Little-endian，0x405c7a82cb20fb22，Data type: double, should convert to floating point,，longitude：113.9142330000000 （dd.dddd format）；
21ea3e00a9953640 --- Little-endian，0x403695a9003eea21， data type: double , should convert to floating point,，longitude：22.5846100000000（dd.dddd format）；
4E --- ASCII code, south and north latitude, the range is /*N or S*/, expressed as: N (north latitude);
45 --- ASCII code, east and west longitude, range is /*E or W*/, expressed as: E (east longitude);
41 --- ASCII code, positioning status, range is /*A or V*/, expressed as: A (valid);
cf084e5f --- Little-endian, 0x5f4e08cf, after Unix timestamp conversion, the value is: 2020/9/1 16:39:43;
13 --- Check code;
2.3 Uplink heart rate and blood pressure（MSGID=0XC2）
Payload contents 
Byte offset	Format	Name	Scale	Unit	Description
2	U16	bp_high	-	-	Systolic blood pressure：2byte
2	U16	bp_low	-	-	Diastolic blood pressure：2byte
2	U16	Bp_heart	-	-	heartrate：2byte
4	Int32	timestamp			timestamp
eg:bdbdbdbdc2000000004800 cf084e5f01
C2 --- MSGID;
0000 --- Little-endian，0x0000，Systolic blood pressure (reserved);
0000 --- Little-endian，0x0000，Diastolic blood pressure (reserved); 
4800 --- Little-endian，0x0048，heartrate 72
cf084e5f —— Timestamp: Beijing time 2020-09-01 16:39:43
01 --- check code 
2.4 Set location reporting Interval（MSGID=0X17）
Byte offset 	Format 	 Name  	Scale 	 Unit 	 Description	　
1	              u8	　enable	-/-	-/-	Enable	Time period 1
2	              U16	 Interval			Time interval（mins）	
1	              u8	time_start_h	　	　	-h	
1	              u8	time_start_m	　	　	-min	
1	              u8	time_end_h	　	　	-h	
1	              u8	time_end_m	　	　	-min	
1	              u8	　enable	-/-	-/-	Enable	Time period 2
2	              U16	Interval			Time Interval（mins）	
1	u8	time_start_h	　	　	-h	
1	u8	time_start_m	　	　	-min	
1	u8	time_end_h	　	　	-h	
1	u8	time_end_m	　	　	-min	
1	u8	　enable	-/-	-/-	enable	Time period 3
1	U16	Interval			Time Interval（mins）	
1	u8	time_start_h	　	　	-h	
1	u8	time_start_m	　	　	-min	
1	u8	time_end_h	　	　	-h	
1	u8	time_end_m	　	　	-min	
1	u8	　enable	-/-	-/-	enable	Time period 4
1	U16	Interval			Time interval（mins）	
1	u8	time_start_h	　	　	-h	
1	u8	time_start_m	　	　	-min	
1	u8	time_end_h	　	　	-h	
1	u8	time_end_m	　	　	-min	
eg：
bdbdbdbd1701030000001300000000000000000000000000000000000000000000dd
0 o'clock to 19 o'clock, location reporting interval is 3 minutes
17 --- MSGID；
01030000001300 --- set reporting interval of Time period 1 
01 --- enable，01 set to enable
0300 --- Reporting Interval，Little Endian representation，0x0030，indicate that the location reporting interval is 3 minutes. 
00 --- time_start_h，0x00，interval time start，0 o'clock. unit：hour
00 --- time_start_m，0x00，interval time start，0 minute. unit：minute
13 --- time_start_h，0x13，interval time end，19o'clock.  unit：hour.
00 --- time_start_m，0x00，cycle time end，0 minute. unit：minute.
000000000000000000000000000000000000000000 --- set reporting interval of time period  2,3,4 ，same as time period 1；
dd --- check

2.5 Uplink SOS message（MSGID=0XB5）
Byte offset	Format	Name	Description
1	U8	Status	status：1:SOS
4	Int	Timestamp	timestamp
Eg: bdbdbdbdb501cf084e5f55
cf084e5f --- Little-endian, 0x5f4e08cf, after Unix timestamp conversion, the value is: 2020/9/1 16:39:43; 
2.6 Uplink Bluetooth location（MsgId=0xD6）
Payload contents:
Format	Name	Scale	Description
U8	type	1	Currently with fixed value”0”
U8	Total_groups	1	The total number of groups, there may be multiple groups and multiple ibeacons in each group
Int32	utc	4	Utc time stamp、Little-endian
U8	Total_PackCount	1	Total number of packages at the current time
U8	Major[0]	2	Major
U8	Minor[0]	2	Minor
U8	Rssi[0]	1	Rssi
U8	Major[1]	2	Major
U8	Minor[1]	2	Minor
U8	Rssi[1]	1	Rssi
Int32	utc	4	Utc time stamp
U8	Total_PackCount	1	Total number of packages at the current time
U8	Major[0]	2	Major
U8	Minor[0]	2	Minor
U8	Rssi[0]	1	Rssi(convert to Int8)
eg：bdbdbdbdd60001be20315f0443271794ac43273094aa4327b956a54327fe94a56a
2.7Uplink alerting message（MsgId=0x02）
Message	LNK-WRN
Description	Terminal uploads its warnings to terminal server.
Firmware	　
Direction	Terminal => Terminal Server
Payload length	2 bytes
Message structure	Header	Message ID	Payload	Checksum
	Token	0x02	See below	CK_sum
Payload contents
Byte Offset	Format	Name	Scale	Unit	Description
2	x16	Upl_warn	-	-	Bitfield see below
4	Int32	Timestamp			timestamp
Bitfield WRN:
15							8				4			1	0

Bit	Name	Description	Code
10	Exit sleep	Exit Sleep Mode	
9	Enter sleep	Enter Sleep Mode	
8	Wearing device		7
7	SOS Exit	Exit SOS mode	8
6			
5			
4	Remove device	Reserved	11
3			
2	Power off	Power off	13
1	SOS		14
0	Low power	Low power	15
eg：Power off the device: BDBDBDBD02040028F2CD5FC1
Lower power alarm: BDBDBDBD02010028F2CD5FC4
2.8 Package without location info（MsgId=0xC7）
Byte offset 	 Format 	 Name  	 Description
1	U16	Status	Package without location info: the displayed value is 0x0020
4	Int32	timestamp	timestamp
eg：BDBDBDBDC7200028F2CD5FAB
2.9 Uplink Temperature info（MsgId=0xBA）
Byte size	Format	Name	Scale	Unit	Description
1	U8	Timestamp identification	required		00 - Time stamped；01 – Non time stamp
4	Int32	Timestamp	Optional		If the timestamp is 01, this field is not required
1	U8	Temperature type	required		1：Indicates uploading surface body temperature and body temperature：
2：Indicates uploading surface body temperature, body temperature and environment temperature
2	S16	surface body temperature	Optional	℃	One digit (×10) is reserved after the decimal point, and the reported value is an integer.
2	S16	body temperature	Optional	℃	One digit (×10) is reserved after the decimal point, and the reported value is an integer.
2	S16	Environment temperature	Optional	℃	One digit (×10) is reserved after the decimal point, and the reported value is an integer.
2.10 Uplink health alarm（MsgId=0x16）
Message	MSG_NB_SOS
Description	Upload health alarm，Include temperature, heart rate alarm
Firmware	-/-
Payload Length	7+4 bytes 
Message structure	Hearer	Message ID	Payload	　
	token	0x16	See definition below	-/-
payload contents
Byte offset	Format	Name	Scale	Unit	Description
1	U8	Type	-/-	-/-	Alarm type: 0: Heart rate alarm
1: Temperature alarm)
2	U16	Heart	-/-	-/-	Heart rate value
2	U16	temperature	-/-	-/-	Temperature value
2	U16	Pa	-/-	-/-	Air pressure value
4	4*U8 or U32	expand	-/-	-/-	Reserved

3. Server to Device Message
3.1 Request time synchronization
Byte offset	Format	Name	Description
1	U8	HEADER	filling：0xFF
1	U8	SeqId	filling：0x00
1	U8	End	filling：0xFF
eg：FF00FF
3.2 Reply to time synchronization request
Byte offset	Format	Name	Description
1	U8	HEADER	filling：0xFF
1	U8	SeqId	filling：0x10
2	U16	years	Year
1	U8	month	Month
1	U8	Day	day
1	U8	time	hour
1	U8	Minute	minute
1	U8	Seconds	seconds
1	U8	End	filling：0xFF
eg：FF1007E409020B1B28FF
FF --- Header
10 --- Seqid
07E4 --- Year，value：2020
09 --- month，value：09
02 --- day，Value：02
0B --- hour，Value：11
1B --- minute，Value：27
28 --- seconds，Value：40
FF --- End 
※Note: After the device is turned on, it will automatically send a time synchronization request. Sync device time after receiving reply.
