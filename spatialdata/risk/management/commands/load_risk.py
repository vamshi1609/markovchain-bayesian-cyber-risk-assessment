from django.core.management.base import BaseCommand
import pandas as pd
from risk.models import Asset, Vulnerability, AssetVulnerability, AssetDependency


class Command(BaseCommand):
    help = "Load cyber-risk dataset (assets, vulns, dependencies) from CSVs"

    def handle(self, *args, **options):
        # Asset–CVE mapping with EPSS and criticality
        try:
            df = pd.read_csv("dataset/vuln_assets.csv")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("dataset/vuln_assets.csv not found"))
            return
        for _, row in df.iterrows():
            asset, created = Asset.objects.get_or_create(
                name=row["asset"],
                defaults={"criticality": row.get("criticality", 5.0)}
            )
            if not created and "criticality" in row:
                asset.criticality = row["criticality"]
                asset.save()
            vuln, _ = Vulnerability.objects.get_or_create(
                cve=row["cve"],
                defaults={"epss_score": row.get("epss_score")}
            )
            AssetVulnerability.objects.get_or_create(asset=asset, vuln=vuln)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(df)} asset–CVE mappings"))
        
        # Asset dependency graph
        try:
            df2 = pd.read_csv("dataset/asset_dependencies.csv")
            for _, row in df2.iterrows():
                src, _ = Asset.objects.get_or_create(name=row["source"])
                tgt, _ = Asset.objects.get_or_create(name=row["target"])
                AssetDependency.objects.get_or_create(
                    source=src,
                    target=tgt,
                    defaults={"weight": row.get("weight", 1.0)}
                )
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(df2)} asset dependencies"))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING("dataset/asset_dependencies.csv not found, skipping"))
