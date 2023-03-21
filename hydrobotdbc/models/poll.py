from ..client import Client
from .collection import Collection


class Poll:
    __tablename__ = 'Polls'

    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, poll_id):
            row = self.client.exec_fetchone(f"SELECT * FROM Polls WHERE PollId={poll_id}")

            return None if row is None else Poll(row.DiscordId, row.Title, row.Options, row.PollId, row.DateRecAdded)

        def filter_by(self, discord_id=None, completed=None):
            sql = "SELECT * FROM PollsQueue "

            allow_multi_clause = False
            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id}"
            if completed is not None:
                sql += f"AND Completed='{completed}' " if allow_multi_clause else f"WHERE Completed='{completed}' "

            sql += "ORDER BY DateRecAdded ASC"

            rows = self.client.exec_fetchall(sql)

            polls = []
            for row in rows:
                polls.append(Poll(poll_id=row.PollId, discord_id=row.DiscordId, title=row.Title,
                                  options=row.Options, winning_options=row.WinningOptions,
                                  winner_votes=row.WinnerVotes, total_votes=row.TotalVotes,
                                  poll_duration=row.PollDuration, completed=row.Completed,
                                  date_rec_added=row.DateRecAdded))

            return Collection(polls)

    query = Query()

    def __init__(self, discord_id, title, options, winning_options, winner_votes, total_votes, poll_duration, completed, poll_id=None, date_rec_added=None):
        self.PollId = poll_id
        self.DiscordId = discord_id
        self.Title = title
        self.Options = options
        self.WinningOptions = winning_options
        self.WinnerVotes = winner_votes
        self.TotalVotes = total_votes
        self.PollDuration = poll_duration
        self.Completed = completed
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
    def options(self):
        return self.Options

    @property
    def winningOptions(self):
        return self.WinningOptions

    @property
    def winnerVotes(self):
        return self.WinnerVotes

    @property
    def totalVotes(self):
        return self.TotalVotes

    @property
    def pollDuration(self):
        return self.PollDuration

    @property
    def completed(self):
        return self.Completed

    @property
    def date_rec_added(self):
        return self.DateRecAdded
