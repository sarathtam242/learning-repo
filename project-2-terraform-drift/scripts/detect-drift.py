import json
import sys
from pathlib import Path


def detect_drift(plan_file: str) -> bool:
    path = Path(plan_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Terraform plan JSON not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        plan = json.load(file)

    if not isinstance(plan, dict) or "resource_drift" not in plan:
        raise ValueError(
            "Invalid Terraform plan JSON: resource_drift field missing"
        )

    drift_items = plan["resource_drift"]

    if not isinstance(drift_items, list):
        raise ValueError(
            "Invalid Terraform plan JSON: resource_drift must be a list"
        )

    print("\n========== TERRAFORM DRIFT REPORT ==========")

    if not drift_items:
        print("DRIFT_DETECTED=false")
        print("No infrastructure drift detected.")
        return False

    print("DRIFT_DETECTED=true")
    print(f"Total resources with drift: {len(drift_items)}")

    for item in drift_items:
        address = item.get("address", "Unknown resource")
        change = item.get("change", {})
        actions = change.get("actions", [])

        print(f"\nResource: {address}")
        print(
            f"Actions: {', '.join(actions) if actions else 'Unknown'}"
        )

    print("\nInfrastructure drift detected!")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect-drift.py <terraform-plan.json>")
        sys.exit(1)

    try:
        detect_drift(sys.argv[1])
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}")
        sys.exit(1)
