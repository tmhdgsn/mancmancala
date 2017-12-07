def log_output(msg):
    with open("output.txt", "a") as f:
        f.write(msg + "\n")