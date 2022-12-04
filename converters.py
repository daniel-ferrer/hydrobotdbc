import models

def ConvertPyodbcToUser(row):
    return models.User(row.DiscordId, row.UserName, row.Discriminator, row.HydroBux, row.Meows)
