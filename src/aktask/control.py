from github import Github
import os


class MainControl:
    def __init__(self):
        pass

    def fill_with_data(self):
        def _list_repos():
            print(str(os.getenv("AKTASK")))
            g = Github("cetoli", str(os.getenv("AKTASK")))
            issues = g.get_user("labase").get_repo("eica").get_issues()
            # Then play with your Github objects:
            for issue in issues:
                _ = ":".join(l.name for l in issue.labels) + ": %s - %d" % (issue.title, issue.number)
        _list_repos()
