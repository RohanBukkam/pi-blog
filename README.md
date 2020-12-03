# Environment Setup
> - Clone [this](https://github.com/rsrahul1000/Pi-Blog.git) repository to pycharm
> - set the interpreter to python 36 venv

> - To setup the venv and install dependency in that env manually, use
> ```bash 
>  python -m venv venv
> .\venv\Scripts\activate
> pip install Flask flask_sqlalchemy rauth Flask-Login Flask-pymysql
> ```
> - use ```pipreqs --force``` to make requirements.txt for the project.
> - ```pip install -r requirements.txt -t lib/```



### For Local Development using pymysql
> - Use: 
> ```SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:GoB3rOvuuEaiuoLt@127.0.0.1:3306/pi_blog_db'```
>> - given that you started the Cloud SQL Proxy with:
>> ```cloud_sql_proxy.exe -instances="pi-blog:asia-south1:pi-blog-sql-instance"=tcp:3306```
> - Test in local using mysqldb
>```SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root:GoB3rOvuuEaiuoLt@127.0.0.1/pi_blog_db?unix_socket=/cloudsql/pi-blog:asia-south1:pi-blog-sql-instance'```

### For Production using pymysql
> - Use:
> ```mysql+pymysql://root:GoB3rOvuuEaiuoLt@/pi_blog_db?unix_socket=/cloudsql/pi-blog:asia-south1:pi-blog-sql-instance```
> - Please make sure to
>> - Add the SQL instance to your ```app.yaml```:  
>> ```beta_settings: cloud_sql_instances: pi-blog:asia-south1:pi-blog-sql-instance```
>> - Enable the SQL Admin API from https://console.developers.google.com/apis/api/sqladmin.googleapis.com/overview