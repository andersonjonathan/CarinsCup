
def get_mysql_credentials(file_path):
    with open(file_path, 'r') as f:
        mysql_credentials = {}
        for line in f:
            fields = line.strip().split()
            mysql_credentials[fields[0]] = fields[1]
        return mysql_credentials
