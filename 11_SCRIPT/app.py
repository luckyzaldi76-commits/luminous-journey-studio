from config import create_folders

from services.production_service import ProductionService
from services.batch_service import BatchService
from services.import_service import ImportService
from services.build_service import BuildService
from services.update_service import UpdateService
from services.backup_service import BackupService
from services.restore_service import RestoreService


class LuminousJourney:

    def __init__(self):

        create_folders()

        self.production = ProductionService()
        self.batch = BatchService()
        self.importer = ImportService()
        self.builder = BuildService()
        self.updater = UpdateService()
        self.backup = BackupService()
        self.restore = RestoreService()

    def menu(self):

        while True:

            print()
            print("=" * 60)
            print("LUMINOUS JOURNEY STUDIO v6")
            print("=" * 60)

            print("1. Production")
            print("2. Batch Production")
            print("3. Import Knowledge")
            print("4. Build Knowledge")
            print("5. Update Dataset")
            print("6. Backup")
            print("7. Restore")
            print("0. Exit")

            choice = input("\nSelect : ").strip()

            if choice == "1":
                self.production.run()

            elif choice == "2":
                self.batch.run()

            elif choice == "3":
                self.importer.run()

            elif choice == "4":
                self.builder.run()

            elif choice == "5":
                self.updater.run()

            elif choice == "6":
                self.backup.run()

            elif choice == "7":
                self.restore.run()

            elif choice == "0":
                print("Bye.")
                break

            else:
                print("Invalid menu.")


if __name__ == "__main__":
    LuminousJourney().menu()