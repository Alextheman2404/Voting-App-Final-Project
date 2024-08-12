import csv
import shutil
import os
from typing import Dict

class VotingData:
    def __init__(self, data_file: str = "data.csv", backup_file: str = "backup_data.csv"):
        """
        Initialize the VotingData with file paths.

        :param data_file: Path to the main data file.
        :param backup_file: Path to the backup data file.
        """
        self.data_file = data_file
        self.backup_file = backup_file
        self.ensure_files_exist()

    def ensure_files_exist(self) -> None:
        """
        Ensure that both data and backup files exist, creating them if necessary.
        """
        if not os.path.isfile(self.data_file):
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", " Vote"])  # Write header to the data file
        if not os.path.isfile(self.backup_file):
            shutil.copy(self.data_file, self.backup_file)  # Create the backup file if it doesn't exist

    def record_vote(self, unique_id: str, vote: str) -> None:
        """
        Record a vote in the data file and update the backup file.

        :param unique_id: Unique identifier for the vote.
        :param vote: The vote (e.g., "John" or "Jane").
        """
        with open(self.data_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([unique_id, f" {vote}"])  # Add a space before the vote
        self.update_backup_file()

    def update_backup_file(self) -> None:
        """
        Update the backup file with the latest data.
        """
        shutil.copy(self.data_file, self.backup_file)

    def validate_id(self, unique_id: str) -> bool:
        """
        Validate if the ID is unique.

        :param unique_id: Unique identifier to validate.
        :return: True if the ID is unique, False otherwise.
        """
        with open(self.data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == unique_id:
                    return False
        return True

    def get_vote_tally(self) -> Dict[str, int]:
        """
        Get the tally of votes.

        :return: A dictionary with vote counts.
        """
        tally = {"John": 0, "Jane": 0}
        with open(self.data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for _, vote in reader:
                if vote.strip() in tally:
                    tally[vote.strip()] += 1
        return tally

    def reset_data(self) -> None:
        """
        Reset the data file and update the backup file.
        """
        with open(self.data_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", " Vote"])  # Write header to the data file
        self.update_backup_file()
