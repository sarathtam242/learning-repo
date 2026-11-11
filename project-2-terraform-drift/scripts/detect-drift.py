import json
import sys


def detect_drift(plan_file):
    try:
        with open(plan_file, "r", encoding="utf-8") as file:
            plan = json.load(file)

        if not isinstance(plan, dict):
            raise ValueError("Invalid Terraform plan structure.")

        # Terraform may omit resource_drift when no drift exists.
        resource_drift = plan.get("resource_drift", [])

        if not isinstance(resource_drift, list):
            raise ValueError("Invalid resource_drift structure.")

        if not resource_drift:
            print("DRIFT_DETECTED=false")
            print("No infrastructure drift detected.")
            return

        print("DRIFT_DETECTED=true")
        print(f"Total drifted resources: {len(resource_drift)}")

        for resource in resource_drift:
            address = resource.get("address", "Unknown resource")
            actions = resource.get("change", {}).get("actions", [])

            print(f"Resource: {address}")
            print(f"Actions: {', '.join(actions)}")

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(f"Drift analysis error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect-drift.py <plan.json>", file=sys.stderr)
        sys.exit(1)

    detect_drift(sys.argv[1])
