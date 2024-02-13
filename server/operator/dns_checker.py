import dns.resolver

class DNSChecker:
    def __init__(self):
        self.mx_records = {}
        self.txt_records = []

    def get_mx(self, domain, retry=3):
        for i in range(retry):
            try: 
                raw_data = dns.resolver.resolve(domain, 'MX')
                for data in raw_data:
                    self.mx_records[str(data.exchange)] = data.preference
                return self.mx_records
            except dns.resolver.NXDOMAIN:
                return f"Domain {domain} does not exist."
            except dns.resolver.NoAnswer:
                return f"No MX records found for domain {domain}."
            except dns.resolver.Timeout:
                # print("DNS query timed out.")
                if i < retry - 1:
                    pass
                    # print("Retrying...")
                else:
                    return "Max retries exceeded."

    def get_txt(self, domain, retry=3):
        for i in range(retry):
            try: 
                raw_data = dns.resolver.resolve(domain, 'TXT')
                for data in raw_data:
                    self.txt_records.append(str(data))
                return self.txt_records
            except dns.resolver.NXDOMAIN:
                return f"Domain {domain} does not exist."
            except dns.resolver.NoAnswer:
                return f"No TXT records found for domain {domain}."
            except dns.resolver.Timeout:
                # print("DNS query timed out.")
                if i < retry - 1:
                    pass
                    # print("Retrying...")
                else:
                    return "Max retries exceeded."

    def verify_mx(self, domain, mx_verify=''):
        mx_results = self.get_mx(domain)
        if isinstance(mx_results, dict) and mx_results:
            for mx, priority in mx_results.items():
                if mx == mx_verify and priority < 20:
                    return True
            return False
        else:
            return mx_results

    def verify_txt(self, domain, user_txt=''):
        txt_results = self.get_txt(domain)
        if isinstance(txt_results, list) and txt_results:
            for txt in txt_results:
                if user_txt in txt:
                    return True
            return False
        else:
            return txt_results

