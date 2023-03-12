from ..client import Client
from .collection import Collection

class PollsQueue:
    __tablename__ = 'PollsQueue'
    class Query:
        def __init__(self):
            self.client = Client()

        def get(self):
            row = self.client.exec_fetchone(f"SELECT * FROM PollsQueue WHERE PollId={id}")

            return None if row is None else PollsQueue(row.PollId, row.DiscordId, row.Title, row.Text, row.Options, row.DateRecAdded)

        def filter_by(self, discord_id=None):
            sql = "SELECT * FROM PollsQueue "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id}"

            sql += "ORDER BY DateRecAdded DESC"

            rows = self.client.exec_fetchall(sql)

            polls = []
            for row in rows:
                polls.append(PollsQueue(row.PollId, row.DiscordId, row.Title, row.Text, row.options, row.DateRecAdded))

            return Collection(polls)

    query = Query()

    def __init__(self, poll_id, discord_id, title, text, options, date_rec_added):
        self.PollId = poll_id
        self.DiscordId = discord_id
        self.Title = title
        self.Text = text
        self.Options = options
        self.DateRecAdded = date_rec_added

    @property
    def id(self):
        return self.PollId

    @property
    def discordId(self):
        return self.DiscordId

    @property
    def title(self):
        return self.Title

    @property
    def text(self):
        return self.Text

    @property
    def options(self):
        return self.Options

    @property
    def date_rec_added(self):
        return self.DateRecAdded