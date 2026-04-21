def parse_access_log(filename):
    import re
    field_names = ("client_ipaddr", "timestamp", 
                       "http_method", "request", 
                       "response_code", "response_size",
                       "referer_url", "user_agent")
    
    Regex = r"""
            (?P<{}>[\d\.]+)      # Extract IP address
            \s-\s-\s
            \[
            (?P<{}>.+?)          # Extract time-stamp 
            \]\s"
            (?P<{}>\w+)          # Extract HTTP method (GET / POST / HEAD)
            \s
            (?P<{}>.+?)          # Extract request/query string
            \sHTTP\/\d\.\d"\s
            (?P<{}>\d+)          # Extract response code
            \s
            (?P<{}>\d+)          # Extract response size
            \s"
            (?P<{}>.+?)          # Extract Referer URL
            "\s"
            (?P<{}>.+?)          # Extract User-Agent (web browser) information
            "\s\d\s\d
    """.format(*field_names)
    
    log_pattern = re.compile(Regex, re.MULTILINE | re.DOTALL | re.VERBOSE)
    
    # logs = []
    with open(filename) as access_log:
        for line in access_log:
            result = log_pattern.match(line)
            if result:
                yield result.groupdict()
                #logs.append(result.groupdict())
    # return logs

if __name__ == '__main__':
    for i, log in zip(range(10), parse_access_log("www.chandrashekar.info.log")):
        print(i, log)
        
    
    


