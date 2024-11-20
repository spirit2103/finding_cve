# Scraper

### Problem Statement
- Web-scrapping tool to be developed to search and report Critical and High Severity Vulnerabilities of OEM equipment (IT and OT) published at respective OEM websites and other relevant web platforms.

### Description 
- Background: Critical Sector organisations uses a number of IT and OT equipment (e.g. Networking and hardware device, Operating Systems, Applications, Firmware etc.). These devices/application come with vulnerabilities from time to time. There should be timely information sharing mechanism by which the concerned equipment users at critical sector orgs should be altered regarding any critical / high severity vulnerabilities in their equipment within the shortest possible time. Detailed description: The ICT components (HW/SW) being used by Critical Sector Organisations become vulnerable from time to time. These vulnerabilities can be categorised as Critical, High, Medium and Low. Any exploitation of these vulnerabilities can cause havoc in multiple Critical Sector Organisations where such vulnerable equipment are being used. Keeping in view of the above, there is a need to monitor all such vulnerability information published at the equipment’s OEM websites and also other relevant websites. Once a critical or high severity vulnerability information is published at OEM website or any other relevant website, the ‘to be developed scrapper’ will immediately take that vulnerability input along with possible mitigating strategy published in the website and send the information to predefined email id(s). Note: The NVD website publishes such OEM vulnerable information. But the same comes with a time lag. It is therefore needed to get such information directly from OEM websites and /or from other relevant websites where such vulnerable information is published almost in real time. Expected Outcome: An automatic script using open source tools to be developed for the OEM vulnerability information scrapping and reporting. Tool should know various vulnerability information published data formats/syntax at OEM websites (both for IT and OT hardware and application) and come up with optimum solution for monitoring and reporting of such vulnerability information. The output of the tool that will be emailed to pre-designated email id(s) is as per following (shared with example; all fields may not be available at the time of reporting): * Product Name: Chrome * Product Version: - NA * OEM name: Google * Severity Level (Critical/High): High * Vulnerability: The N-able PassPortal extension before 3.29.2 for Chrome inserts sensitive information into a log file. * Mitigation Strategy: Install patch from https://me.n-able.com/s/security-advisory/aArHs000000M8CCKA0/cve202347131-passportal-browser-extension-logs-sensitive-data * Published Date: Jan 2024 * Unique ID: CVE-2023-47131


### Approach
- [ ] A scraper module that uses scrapy to scrape the vendor specific oem sites and relevant sites
- [ ] Clean the data and store it into database, prefer mongodb
- [ ] Configure config.yaml file and stores all the neccessary credentials there
- [ ] Setup logging to log info for further debugging
- [ ] Check for the repetition of data
- [ ] Create a scheduler that will run the script every midnight use UST or IST
- [ ] In the backend nodejs will directly access the database

### Features to be add


### Scalability


## IT
### API based OEM sites
- [ ] National Vulnerability Database - https://nvd.nist.gov
- [ ] CVE Program API - https://www.cve.org
- [ ] Explot-db- https://www.exploit-db.com
- [ ] Tenable.io API - https://developer.tenable.com/reference/navigate
- [ ] Rapid7 Insight Platform API - https://help.rapid7.com/insightvm/en-us/api/index.html
- [ ] REDHAT : https://docs.redhat.com/en/documentation/red_hat_security_data_api/1.0/html/red_hat_security_data_api/cve#list_all_cves
- [ ] VULDB : https://vuldb.com/
- [ ] Americas cyber defence agency: https://www.cisa.gov/known-exploited-vulnerabilities-catalogi
- [ ] OSV : https://google.github.io/osv.dev/api/
- [ ] IBM x-force intelligence: https://api.xforce.ibmcloud.com/doc/#api_section
- [ ] SHODAN: https://developer.shodan.io/api
- [ ] GITHUB docs: https://docs.github.com/en/graphql/overview/explorer

### Manual Scraping Platforms

- [ ] CVE Details - https://www.cvedetails.com

- [ ] SecurityFocus (BugTraq Archive) - http://www.securityfocus.com/vulnerabilities

- [ ] CERT/CC Vulnerability Notes Database - https://www.kb.cert.org/vuln/

- [ ] Global security database: https://gsd.id/getting-started

- Vendor-Specific Sites
  - [ ] Microsoft: https://msrc.microsoft.com/update-guide
  - [ ] NVIDIA : https://www.nvidia.com/en-us/security/
  - [ ] INTEL : https://www.intel.com/content/www/us/en/security-center/default.html
  - [ ] DELL : https://www.dell.com/support/security/en-us
  - [ ] APPLE : https://support.apple.com/en-us/100100
  - [ ] GOOGLE security-bulletins: https://source.android.com/docs/security/bulletin
  - [ ] REDHAT : https://access.redhat.com/security/security-updates/
  - [ ] UBUNTU : https://ubuntu.com/security/notices
  - [ ] APACHE : https://security.apache.org/projects/
  - [ ] ADOBE : https://helpx.adobe.com/security/security-bulletin.html
  - [ ] ORACLE : https://www.oracle.com/security-alerts/
  - [ ] CISCO : https://sec.cloudapps.cisco.com/security/center/publicationListing.x
  - [ ] VMWARWE : https://www.broadcom.com/support/vmware-security-advisories

- [ ] MITRE ATT&CK - https://attack.mitre.org

## OT

- [ ] Scheneider electric: https://www.se.com/ww/en/work/support/cybersecurity/security-notifications.jsp
                          - https://www.se.com/ww/en/work/support/cybersecurity/security-notifications-archive.jsp
