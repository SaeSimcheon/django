# Make RDS parameter group

![image](https://user-images.githubusercontent.com/49121293/161899442-ff976b8e-d080-4000-b4a9-e72a402fc0a8.png)

![image](https://user-images.githubusercontent.com/49121293/161899544-3ecf1c77-5109-4e6d-91c4-2238ab825751.png)

## Search 'character' and then edit parameter.
- Except for the parameters which are numeric, set the parameters as utf8.


# Make RDS instance.

![image](https://user-images.githubusercontent.com/49121293/161900486-abb3f64e-bfcd-446f-8139-b9639ae3977f.png)

![image](https://user-images.githubusercontent.com/49121293/161900229-b1c03289-1f00-4c53-84d4-54023bfa16df.png)


- Note that DB instance ID is not DB name
- Before migrating db, add public ip to inbound rule in VPC security group.




# Configration for AWS RDS

- In config/settings.py
- I used pymysql.



```python
import pymysql
pymysql.version_info = (1,4,2,"final",0)
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB name',
        'USER': 'user name',
        "PASSWORD" : "password of user",
        "HOST" : "end point of DB ",
        "PORT" : '3306',
    }
}
```


# S3 media server

## Make a bucket.
