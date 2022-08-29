import pandas as pd


class SocialNetworkMatrix:
    def __init__(self, df):
        self.df = df

    @classmethod
    def build_from_dict(self, dictionary):
        df = pd.DataFrame()
        for username, followers in dictionary.items():
            for follower in followers:
                df.loc[username, follower["username"]] = 1
        return SocialNetworkMatrix(df.T)



