from django.core.management.base import BaseCommand

from predictor.ml_model.train import train_and_save


class Command(BaseCommand):
    help = "Train the career prediction model and save it as predictor/ml_model/career_model.pkl"

    def handle(self, *args, **options):
        model_path = train_and_save()
        self.stdout.write(self.style.SUCCESS(f"Model trained and saved to: {model_path}"))
