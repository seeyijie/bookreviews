def getIP(instance_type):
    if instance_type == 'localhost':
        print(f"Using localhost")
        return instance_type
    elif instance_type == 'flask':
        f = open("../scripts/server_scripts/config/config_flask_ip.txt", "r")
        ip = f.readline()
        f.close()
        print(f"IP for Flask service is {ip}")
        return ip
    elif instance_type == 'mongodb':
        f = open("../scripts/server_scripts/config/config_mongodb_ip.txt", "r")
        ip = f.readline()
        f.close()
        print(f"IP for MongoDB service is {ip}")
        return ip
    elif instance_type == 'mysql':
        f = open("../scripts/server_scripts/config/config_mysql_ip.txt", "r")
        ip = f.readline()
        f.close()
        print(f"IP for MYSQL service is {ip}")
        return ip

