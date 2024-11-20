import yaml
import requests


class VulnerabilityMonitor:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the vulnerability monitor system"""
        self.config = self._load_config(config_path)
        self._setup_logging()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def _setup_logging(self):
        """
        Configure logging 
        """
        self.logger = logging.getLogger("VulnerabilityMonitor")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %{levelname}s - %{message}s", filename=self.config['logging']['file_path'])


    def scrape_vendor_page(self, vendor_config: Dict) -> List[Dict]:
        """
        Scrape vulnerability info from vendor oem page.
        Returns list of vulnerability dictionaries
        """
        vulnerabilities = []
        
        try:
            response = requests.get()

obj = VulnerabilityMonitor("config.yaml") # default value
print(obj)
