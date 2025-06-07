# รัน docker
1. โหลดโฟลเดอร์
2. run Docker
3. เปิด cmd หรือ powershell change work directory ที่โฟลเดอร์ที่เก็บไฟล์ไว้ เช่น เก็บไฟล์ไว้ในโฟลเดอร์ D:\DADS5001 ใช้ `cd D:\DADS5001` หรือ กรณีอยู่คนละไดรฟ์ ใช้ `cd /d D:\DADS5001`
4. กรณีเริ่มใช้งานครั้งแรก รัน command นี้ `docker-compose -f final\docker-compose.yml up --build` ใน cmd หรือ powershell โดย final\docker-compose.yml คือที่อยู่ไฟล์ docker-compose.yml \
กรณีใช้งานครั้งถัดไป หากไม่มีการแก้ไข รัน command นี้ `docker-compose up -f final\docker-compose.yml up`
5. หยุดการใช้งานโดย Ctr+C หรือ `docker-compose down`
