import os

for i in range(300):
    print(i)
    with open("output.txt", "a+") as fp:
        fp.write(str(i) + "\n")
    os.system("python3 debug3.py")
