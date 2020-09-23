import dateutil.parser


class APIModel:
    data = {}

    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data.get(name)
        raise AttributeError


class Barrier(APIModel):

    @property
    def is_resolved_text(self):
        if self.is_resolved:
            if self.status_date:
                return f"Yes - {self.status_date.strftime('%B %Y')}"
            return "Yes"
        return "No"

    @property
    def status_date(self):
        if self.data.get("status_date"):
            return dateutil.parser.parse(self.data["status_date"])

    @property
    def country(self):
        return self.data["country"].get("name")

    @property
    def location(self):
        return self.data["location"]

    @property
    def sectors(self):
        return ", ".join(self.sectors_list)

    @property
    def sectors_list(self):
        sector_names = [s.get("name") for s in self.data.get("sectors", {})]
        return sector_names

    @property
    def categories_list(self):
        return [s.get("name") for s in self.data.get("categories", {})]

    @property
    def public_id(self):
        return f"PID-{self.id}"
