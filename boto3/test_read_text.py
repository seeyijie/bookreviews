ip = "10.0.0.2"

f = open("../scripts/server_scripts/config/demofile2.txt", "r")
ip = f.readline()
f.close()

print(f"ip read was {ip}")