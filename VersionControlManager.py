# Class to represent one version of a file
class Version:
    def __init__(self, version_number, content):
        self.version_number = version_number  # Which version
        self.content = content  # Full content of the file

# Main class to simulate the Version Control System
class VersionControlSystem:
    def __init__(self):
        self.versions = []  # Stores all committed versions
        self.current_version = -1  # Tracks the latest version number

    def commit(self, content):
        """
        Commit a new version of the file.
        """
        self.current_version += 1  # Increment version number
        new_version = Version(self.current_version, content)  # Create new version object
        self.versions.append(new_version)  # Save the version
        print(f"Committed version {self.current_version}")
        return self.current_version

    def get(self, version_number):
        """
        Retrieve file content of a given version number.
        """
        if 0 <= version_number < len(self.versions):
            return self.versions[version_number].content
        else:
            return "Version not found"

    def log(self):
        """
        Print the version history.
        """
        print("Version History:")
        for version in self.versions:
            print(f"Version {version.version_number}: {version.content[:30]}...")

    def revert(self, version_number):
        """
        Revert current version to a previous one.
        """
        if 0 <= version_number < len(self.versions):
            reverted_content = self.versions[version_number].content
            return self.commit(reverted_content)  # Save reverted as a new commit
        else:
            print("Version not found")
            return None

    def diff(self, v1, v2):
        """
        Compare content between two versions line by line.
        """
        if not (0 <= v1 < len(self.versions) and 0 <= v2 < len(self.versions)):
            print("One of the versions does not exist")
            return

        content1 = self.versions[v1].content.splitlines()
        content2 = self.versions[v2].content.splitlines()

        print(f"Diff between version {v1} and {v2}:")
        for i in range(max(len(content1), len(content2))):
            line1 = content1[i] if i < len(content1) else ""
            line2 = content2[i] if i < len(content2) else ""
            if line1 != line2:
                print(f"- {line1}")
                print(f"+ {line2}")
