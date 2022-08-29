from cleaner import SocialNetworkMatrix

sample_sn = {
    "vale": ["luisa", "ma", "jose", "sebas", "nata", "ligia"],
    "luisa": ["ma", "nata", "angela", "ligia"],
    "ma": ["luisa", "vale", "nata", "ligia"],
    "jose": ["sebas", "marta", "carlos"],
    "sebas": ["jose"]
}


def test_build_from_dict():
    sample_sn_dict = {}
    for username, followers in sample_sn.items():
        sample_sn_dict[username] = [{"username": follower} for follower in followers]
    snm = SocialNetworkMatrix.build_from_dict(sample_sn_dict)
    for username in sample_sn.keys():
        assert len(sample_sn[username]) == snm.df[username].sum()
